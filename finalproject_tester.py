from finalproject import*

# *** QUESTION 1 *** #


def average_month_kwh_data_tester():
    """
    runs a series of tests for average_month_kwh_data
    :return: (bool) were all tests successful
    """
    # check accuracy
    assert average_month_kwh_data("energy-usage-2010.csv", 4) == 14584
    assert average_month_kwh_data("energy-usage-2010.csv", 10) == 16227

    # check type
    assert type(average_month_kwh_data("energy-usage-2010.csv", 4)) == int

    return True


def average_season_kwh_data_tester():
    """
    runs a series of tests for average_season_kwh_data
    :return: (bool) were all tests successful
    """
    assert average_season_kwh_data(4, 5, 15) == 15287
    assert average_season_kwh_data(9, 10, 11) == 16071
    assert type(average_season_kwh_data(9, 10, 11)) == int

    return True


def average_energy_list_tester():
    """
    runs a series of tests for average_energy_list
    :return: (bool) were all tests successful
    """
    assert type(average_energy_list()) == list
    assert type(average_energy_list()[0]) == int

    return True


# *** QUESTION 2 *** #


def test_parse_income_data():
    """
    Runs a series of tests for parse_income_data
    :return: (bool) were all tests successful
    """
    # check accuracy
    assert parse_income_data("incomeTEST.csv") == {"Rogers Park": 23939, "West Ridge": 23040, "Uptown": 35787, }

    # check type
    assert type(parse_income_data("incomeTEST.csv")) == dict

    income_data = parse_income_data("socioeconomic.csv")
    for key, value in income_data.items():
        # check the data type of the return values
        assert type(key) == str
        assert type(value) == int

    return True


def test_parse_energy_data():
    """
    Runs a series of tests for parse_energy_data
    :return: (bool) were all tests successful
    """
    # only creates data entries if all necessary data is present
    assert parse_energy_data("parse_energyTEST.csv") == [('Ashburn', 732.7142857142857)]
    assert type(parse_energy_data("energy-usage-2010.csv")) == list

    energy_data = parse_energy_data("energy-usage-2010.csv")
    for item in energy_data:
        count = 0
        for tuple in item:
            # check the data type of the return values
            if count == 0:
                assert type(tuple) == str
            else:
                assert type(tuple) == float
            count += 1

    return True


def test_income_and_energy_correlate_data():
    """
    Runs a series of tests for income_and_energy_correlate_data
    :return: (bool) were all tests successful
    """
    all_income = parse_income_data("socioeconomic.csv")  # all income data
    income1 = parse_income_data("incomeTEST.csv")  # income entries with no community names matching to energy1
    income2 = parse_income_data("incomeTEST2.csv")  # income entries with all matching names to energy1
    energy1 = parse_energy_data("parse_energyTEST.csv")  # energy entries with data missing
    energy2 = parse_energy_data("parse_energyTEST2.csv")  # energy entries with no relevant data missing

    # check that the list doesn't make entries if community names don't match up
    assert income_and_energy_correlate_data(income1, energy1) == []

    # check that the list doesn't makes entries if data values are 0 or missing
    assert income_and_energy_correlate_data(income2, energy1) == [[23482, 732.7142857142857]]

    # check that it works when all names and values are approved
    assert len(income_and_energy_correlate_data(all_income, energy2)) == 3
    assert income_and_energy_correlate_data(all_income, energy2) == [[11888, 63.757894736842104],
                                                                     [71551, 256.8032786885246],
                                                                     [88669, 900.8055555555555]]

    # check the type of the items in the returned list
    assert type(income_and_energy_correlate_data(all_income, energy2)[0][0]) == int
    assert type(income_and_energy_correlate_data(all_income, energy2)[0][1]) == float

    return True


def test_spearman_income_and_energy():
    """
    Runs a series of tests for spearman_income_and_energy
    :return: (bool) were all tests successful
    """
    test_lst = [[1, 2], [3, 4], [5, 6]]

    spearman = spearman_income_and_energy(test_lst).tolist()

    # check for accuracy of the
    assert spearman == [[1.0, 1.0], [1.0, 1.0]]

    return True

# *** QUESTION 3 *** #


def test_parse_energy_for_apartments():
    """
    Runs a series of tests for parse_energy_for_apartments
    :return: (bool) were all tests successful
    """
    # check that it doesn't create a data entry if the data is 0 or nothing for the specified columns
    assert parse_energy_for_apartments("parse_energyTEST2.csv") == [[2.0820042530568847], [5.5873535492763615]]

    # check that it returns a list
    assert type(parse_energy_for_apartments("parse_energyTEST2.csv")) == list

    # check that its a list of lists
    assert type(parse_energy_for_apartments("parse_energyTEST2.csv")[0]) == list

    # check that its a list of lists of floats
    assert type(parse_energy_for_apartments("parse_energyTEST2.csv")[0][0]) == float

    return True


def test_parse_energy_for_apartments_helper():
    """
    Runs a series of tests for parse_energy_for_apartments_helper
    :return: (bool) were all tests successful
    """
    test_list1 = [['Building', 5], ['Building 1', 6], ['Building 2', 9]]
    test_list2 = [['Multi 7+', 5], ['Multi 7+', 6], ['Multi < 7', 9]]

    # check that it doesn't add anything if the building sub-type is incorrect
    assert parse_energy_for_apartments_helper(test_list1) == [[], []]

    # check for accuracy
    assert parse_energy_for_apartments_helper(test_list2) == [[5, 6], [9]]

    # check that it returns a list
    assert type(parse_energy_for_apartments_helper(test_list2)) == list

    # check that it returns a list of lists of floats
    helper = parse_energy_for_apartments_helper(test_list2)
    for item in helper:
        if type(item) != list:
            return False
        for data in item:
            if type(data) != float and type(data) != int:
                return False

    return True


def test_energy_efficiency_medians():
    """
    Runs a series of tests for energy_efficiency_medians
    :return: (bool) were all tests successful
    """
    test_lst = [[1, 2, 3, 4], [5, 6, 7, 8, 9]]

    # check that the median can be calculated for even and odd length lists
    assert energy_efficiency_medians(test_lst) == [2.5, 7]

    # check that the medians are returned in a list
    assert type(energy_efficiency_medians(test_lst)) == list

    # check the length
    assert len(energy_efficiency_medians(test_lst)) == 2

    return True


def main():
    print("test average_month_kwh_data() ... " + "PASS" if average_month_kwh_data_tester() else "FAIL")
    print("test average_season_kwh_data() ... " + "PASS" if average_season_kwh_data_tester() else "FAIL")
    print("test average_energy_list() ... " + "PASS" if average_energy_list_tester() else "FAIL")
    print("test parse_income_data ... " + "PASS" if test_parse_income_data() else "FAIL")
    print("test parse_energy_data ... " + "PASS" if test_parse_energy_data() else "FAIL")
    print("test income_and_energy_correlate_data ... " + "PASS" if test_income_and_energy_correlate_data() else "FAIL")
    print("test spearman_income_and_energy ..." + "PASS" if test_spearman_income_and_energy() else "FAIL")
    print("test parse_energy_for_apartments ... " + "PASS" if test_parse_energy_for_apartments() else "FAIL")
    print("test energy_efficiency_medians ... " + "PASS" if test_energy_efficiency_medians() else "FAIL")
    print("test parse_energy_for_apartments_helper ... " + "PASS" if test_parse_energy_for_apartments_helper() else "FAIL")


if __name__ == "__main__":
    main()