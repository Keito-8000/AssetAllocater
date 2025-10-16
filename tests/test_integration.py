import os
from assetallocater import load_assets, load_allocations

def test_e2e_allocation_with_temp_csv_files(tmp_path):
    """
    READMEの使用例に基づいたエンドツーエンドのテスト。
    pytestのtmp_path fixtureを使用して一時的なCSVファイルを作成してテストする。
    """
    # --- Setup: 一時ファイルを作成 ---
    assets_csv_path = tmp_path / "assets.csv"
    assets_csv_path.write_text(
        "name,principal,value\n"
        "オルカン,100000,120000\n"
        "S&P500,50000,60000\n",
        encoding="utf-8"
    )

    allocations_csv_path = tmp_path / "allocations.csv"
    allocations_csv_path.write_text(
        "name,class,ratio\n"
        "オルカン,米国株式,0.7\n"
        "オルカン,新興国株式,0.3\n"
        "S&P500,米国株式,1.0\n",
        encoding="utf-8"
    )

    # --- Execution ---
    assets = load_assets(str(assets_csv_path))
    allocations = load_allocations(str(allocations_csv_path))
    result = allocations * assets

    # --- Verification ---
    expected_values = {
        "米国株式": 144000.0,
        "新興国株式": 36000.0,
    }
    expected_principals = {
        "米国株式": 120000.0,
        "新興国株式": 30000.0,
    }

    assert len(result.values) == len(expected_values)
    for cls, value in expected_values.items():
        assert abs(result.values[cls] - value) < 1e-9

    assert len(result.principals) == len(expected_principals)
    for cls, value in expected_principals.items():
        assert abs(result.principals[cls] - value) < 1e-9

    assert abs(result.total_value() - 180000.0) < 1e-9


def test_e2e_allocation_from_fixed_csv_files():
    """
    固定のテスト用CSVファイルを読み込んでテストする。
    """
    # --- Setup: ファイルパスを解決 ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_csv_path = os.path.join(current_dir, "data", "assets.csv")
    allocations_csv_path = os.path.join(current_dir, "data", "allocations.csv")

    # --- Execution ---
    assets = load_assets(assets_csv_path)
    allocations = load_allocations(allocations_csv_path)
    result = allocations * assets

    # --- Verification ---
    expected_values = {
        "米国株式": 144000.0,
        "新興国株式": 36000.0,
    }
    expected_principals = {
        "米国株式": 120000.0,
        "新興国株式": 30000.0,
    }

    assert len(result.values) == len(expected_values)
    for cls, value in expected_values.items():
        assert abs(result.values[cls] - value) < 1e-9

    assert len(result.principals) == len(expected_principals)
    for cls, value in expected_principals.items():
        assert abs(result.principals[cls] - value) < 1e-9


def test_e2e_decompose_olcan_estimated():
    """
    オルカン（推定・按分した構成比）を分解するテスト。
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_csv_path = os.path.join(current_dir, "data", "assets_olcan.csv")
    allocations_csv_path = os.path.join(current_dir, "data", "allocations_olcan_estimated.csv")

    assets = load_assets(assets_csv_path)
    allocations = load_allocations(allocations_csv_path)
    result = allocations * assets

    # 期待値の計算 (元本100万円)
    total_value = 1000000
    expected_values = {
        "日本株式": total_value * 0.049,
        "先進国株式（除く日本）": total_value * 0.883,
        "新興国株式": total_value * 0.068,
    }

    assert len(result.values) == len(expected_values)
    for cls, value in expected_values.items():
        assert abs(result.values[cls] - value) < 1e-9


def test_e2e_decompose_olcan_top10_with_undefined():
    """
    オルカン（上位10カ国）を分解し、残りがundefinedとして補完されることをテストする。
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_csv_path = os.path.join(current_dir, "data", "assets_olcan.csv")
    allocations_csv_path = os.path.join(current_dir, "data", "allocations_olcan_top10.csv")

    assets = load_assets(assets_csv_path)
    allocations = load_allocations(allocations_csv_path) # ここでundefinedが補完される
    result = allocations * assets

    # 期待値の計算 (元本100万円)
    total_value = 1000000
    expected_values = {
        "アメリカ": total_value * 0.64,
        "日本": total_value * 0.049,
        "イギリス": total_value * 0.032,
        "カナダ": total_value * 0.028,
        "フランス": total_value * 0.023,
        "ドイツ": total_value * 0.022,
        "スイス": total_value * 0.021,
        "台湾": total_value * 0.019,
        "ケイマン諸島": total_value * 0.019,
        "インド": total_value * 0.017,
        "undefined": total_value * (1.0 - 0.87),
    }

    assert len(result.values) == len(expected_values)
    for cls, value in expected_values.items():
        assert abs(result.values[cls] - value) < 1e-9
