"""
    CS051P Lab Assignments: Final Project

    Author: Hannah Mandell & Kirsten Housen

    Date: 12 - 13 - 19

    This program displays control over csv file usage, matplotlib, and function creation to better understand numerical
    data within large data files. More specifically, this program analyzes Chicago csvs of KWH energy usage and
    determines whether, on average, more energy is used in the winter months or the summer months and creates a scatter
    plot of Month of the Year v. Average Energy Usage. This program also analyzes Chicago csvs of socioeconomic factors
    and residential building energy usage and attempts to find a correlation by drawing a scatter plot of
    Average Community Income vs. Personal Energy Consumption (kw/person/year)
"""
import matplotlib.pyplot as plt
import numpy as np
from numpy import median
from scipy import stats

# *** QUESTION 1: Is more energy used in the winter or summer? *** #


def average_month_kwh_data(fname, list_index_of_month):
    """
    Takes a csv file of Chicago KWH energy data for the index of the month specified a returns the average KWH usage
    for that month
    :param fname: (str) name of a csv file containing KWH energy usage
    :return: (int) the average KWH used in Chicago during the month specified
    """
    # open file
    file_in = open(fname, "r")

    # create a count
    kwh_count = 0

    # skip the first line of the file because it only includes the column titles
    file_in.readline()

    # for the rest of the lines in the file:
    for line in file_in:

        # do nothing for the last line of the file because it is whitespace
        if line == "\n":
            continue

        # turn the list into a list of data values
        data_lst = line.split(",")

        # only create data entries for month specified
        # add each data value to the kwh_count
        for i in data_lst[list_index_of_month]:
            kwh_count += int(i)

        # average the count and cast to an int
        kwh_average = int(kwh_count/len(data_lst))

    # close the file
    file_in.close

    # Return the average kwh useage
    return kwh_average


def average_energy_list():
    """
    This function creates a list of the average energy for each month of the year from the Chicago data set.
    :return: (lst) a list of average energies
    """
    # create energy list
    energy_list = []
    for i in range(4,16):
        energy = average_month_kwh_data("energy-usage-2010.csv", i)
        energy_list.append(energy)
    return energy_list


def scatter_plot(format):
    """
    This function plots the data from average_energy_list relative to the corresponding month of the year
    :param format: (str) specifies the color and format of the data
    :return: (none)
    """
    # create month list
    month_list = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]

    # get energy list
    energy_list = average_energy_list()

    # plot the data
    plt.plot(month_list, energy_list, format)

    # label the x and y axis
    plt.xlabel("Month")
    plt.ylabel("Average Energy Usage (KWH)")

    # title the plot
    plt.title("Month of the Year v. Average Energy Usage in Chicago")

    # display the plot with the legend
    plt.legend(["Average Energy Usage"])

    plt.savefig("visualization1.png")

    plt.show()


def average_season_kwh_data(month_1_index, month_2_index, month_3_index):
    """
    This function takes three parameters, each an index of the month that data is wanted for, and returns the average
    KWH energy usage over those three months
    :param month_1_index: (int) index of the first month that data is wanted for
    :param month_2_index: (int) index of the second month that data is wanted for
    :param month_3_index: (int) index of the third month that data is wanted for
    :return: (int) the average KWH usage over the three months inputted
    """
    # Gather data for each month inputted
    average_data_month_1 = average_month_kwh_data("energy-usage-2010.csv", month_1_index)
    average_data_month_2 = average_month_kwh_data("energy-usage-2010.csv", month_2_index)
    average_data_month_3 = average_month_kwh_data("energy-usage-2010.csv", month_3_index)

    # Average data
    total_average = int((average_data_month_1 + average_data_month_2 + average_data_month_3)/3)

    # Return total_average
    return total_average


# *** QUESTION 2: Do people in higher earning communities use more energy at home? *** #


def parse_income_data(fname):
    """
    Takes a csv file of Chicago census data and returns a dictionary of {str(community name): int(average income)}
    :param fname: (str) name of a csv file containing Chicago socioeconomic census data
    :return: (dict) a dictionary of ints that represent the average income of a community
    """
    # open the file
    file_in = open(fname, "r")

    # create an empty dictionary to put the community names and income data into
    income_dict = {}

    # skip the first line of the file because it only includes the column titles
    file_in.readline()

    # for the rest of the lines in the file:
    for line in file_in:

        # turn the list into a list of data values
        data_lst = line.split(",")

        # create a dictionary entry for the community name and its income
        community_name = data_lst[1]
        income_dict[community_name] = int(data_lst[7])

        # clear data_lst so that it can be used for the next line of the file
        data_lst.clear()

    # close the file
    file_in.close()

    # return the dictionary of community names and incomes
    return income_dict


def parse_energy_data(fname):
    """
    Takes a csv file of Chicago building energy data and returns a dictionary of {community name: annual individual
    energy usage (kw/person)}
    :param fname: (str) name of a csv file containing Chicago building energy data
    :return: (list) a list of tuples with the data (community name, average individual energy use (kw/person) in the
    residential building)
    """
    # open the file
    file_in = open(fname, "r")

    # create an empty list to put all of the
    energy_list = []

    # skip the first line of the file because it only includes the column titles
    file_in.readline()

    # go through each line in the file
    for line in file_in:

        # do nothing for the last line of the file because it's just whitespace
        if line == "\n":
            continue

        # turn the line into a list of data
        data_lst = line.split(",")

        # only create data entries for residential buildings
        if data_lst[2] != "Residential":
            continue

        # if there is an empty data entry or the data is 0, don't create a dictionary entry
        if data_lst[0] == "" or data_lst[16] == "" or data_lst[16] == "0" or data_lst[63] == "" or data_lst[63] == "0":
            continue

        # if all the appropriate data is present:
        else:

            # assign variable names for clarity
            community_name = data_lst[0]
            total_building_kwh = float(data_lst[16])
            total_building_population = float(data_lst[63])

            # calculate the energy usage in kwh/person for each entry
            kwh_per_person = total_building_kwh/total_building_population

            # append the community name and average individual energy use to energy_list
            energy_tuple = (community_name, kwh_per_person)
            energy_list.append(energy_tuple)

    # close the file
    file_in.close()

    # return the list of tuples
    return energy_list


def income_and_energy_correlate_data(income_dict, energy_list):
    """
    Takes an income_dict and an energy_dict and returns a list of data containing average income and average annual
    kw/person energy use
    :param income_dict: (dict) a dictionary mapping community name strings to ints representing the average income of
    the community
    :param energy_list: (list) a list of lists with the data [community name: annual energy usage (kw/person) of a
    residential building]
    :return: (list) a list where each item represents a [average income, annual energy usage (kw/person) of a
    residential building] pair
    """
    # create an empty list to put the income and energy use data into
    correlate_data_lst = []

    # go through each tuple in energy_list
    for energy_tuple in energy_list:
        community = energy_tuple[0]
        building_energy = energy_tuple[1]

        # if the community name is a key in income_dict
        if community in income_dict.keys():
            avg_income = income_dict[community]

            # append an item of (the community's avg income, the building's annual energy consumption (kw/person)) to
            # correlate_data_lst
            correlate_data_lst.append([avg_income, building_energy])

    # return the list of lists
    return correlate_data_lst


def spearman_income_and_energy(correlated_data):
    """
    Takes two list of related data and returns a Spearman correlation
    :param correlated_data: (list) list of lists of [average income, annual energy usage (kw/person) of a residential building]
    :return: (list) a list where each item represents [average income, annual energy usage (kw/person) of a residential building]
    """
    income_values = []
    energy_values = []

    # go through each nested list in the data list
    for data_tuple in correlated_data:
        index = 0

        # go through the data set in the nested list
        for value in data_tuple:

            # append the avg income data to the income_value list
            if index == 0:
                income_values.append(value)

            # append the energy data to the energy_value list
            else:
                energy_values.append(value)
            index += 1

    # calculate the Spearman correlation for average community income and personal energy use
    spearman_corr = np.corrcoef(income_values, energy_values)

    # return the Spearman correlation
    return (spearman_corr)


def plot_income_and_energy(data, format):
    """
    Plots the data in <data>, showing average income on the x-axis and a building's annual energy consumption in
    kw/person on the y-axis. Will only display the plot and the legend if <done> is True
    :param data: (list) a list where each entry is a list of [avg annual income of a community, annual energy usage
    (kw/person) of a residential building in that community]
    :param format: (str) a matplotlib format string
    """
    # put the corresponding x (income) and y (energy) data into separate lists
    income_values = []
    energy_values = []

    # go through each nested list in the data list
    for data_tuple in data:
        index = 0

        # go through the data set in the nested list
        for value in data_tuple:

            # append the avg income data to the income_value list
            if index == 0:
                income_values.append(value)

            # append the rain data to the rain_value list
            else:
                energy_values.append(value)
            index += 1

    # plot the data
    plt.plot(income_values, energy_values, format, label = "Residential Household")

    # label the x and y axis
    plt.xlabel("Average Community Income ($)")
    plt.ylabel("Personal Energy Usage (kw/person/year)")

    # title the plot
    plt.title("Average Community Income v. Personal Energy Usage in Chicago Communities")

    # display the plot
    plt.legend()

    plt.savefig("visualization2.png")

    plt.show()


# *** QUESTION 3: Are low-rise apartment buildings more energy efficient than high-rise apartment buildings? *** #


def parse_energy_for_apartments(fname):
    """
    Takes a csv energy file and returns a list of tuples containing building sub-type and energy efficiency
    :param fname: (str) name of a csv file containing Chicago building energy data
    :return: (list) a list of lists of [building sub-type, energy efficiency (kw/sq feet)]
    """
    # open the file
    file_in = open(fname, "r")

    # create an empty list to put all of the lists into
    building_efficiency_list = []

    # skip the first line of the file because it only includes the column titles
    file_in.readline()

    # go through each line in the file
    for line in file_in:

        # do nothing for the last line of the file because it's just whitespace
        if line == "\n":
            continue

        # turn the line into a list of data
        data_lst = line.split(",")

        # only create data entries for residential buildings
        if data_lst[2] != "Residential":
            continue

        # only create data entries for residential multifamily buildings
        if data_lst[3] != "Multi 7+" and data_lst[3] != "Multi < 7":
            continue

        # only create data entries for residential multifamily buildings with 1 or more floors
        if float(data_lst[65]) < 1:
            continue

        # if the data entry is empty or 0 for the building sub-type, total kwh, kwh sq feet, don't create a data entry
        if data_lst[3] == "" or data_lst[16] == "" or data_lst[16] == "0" or data_lst[33] == "" or data_lst[33] == "0":
            continue

        # if all the appropriate data is present:
        else:

            # assign variable names for clarity
            building_sub_type = data_lst[3]
            total_building_kwh = float(data_lst[16])
            sq_ft = float(data_lst[33])

            # calculate the energy efficiency in kw/square feet
            kwh_per_sq_ft = total_building_kwh/sq_ft

            # append the building sub-type and energy efficiency use to energy_efficiency_list
            building_list = [building_sub_type, kwh_per_sq_ft]
            building_efficiency_list.append(building_list)

    # call the helper function to turn energy_efficiency_list into lists of energy efficiency values for each building sub-type
    efficiency_values_list = parse_energy_for_apartments_helper(building_efficiency_list)

    # close the file
    file_in.close()

    # return the list of lists of efficiency values
    return efficiency_values_list


def parse_energy_for_apartments_helper(building_efficiency_list):
    """
    Takes a list of lists of [building sub-type, energy efficiency (kw/sq ft)] and returns a list that contains 2 lists:
    One list of energy efficiency values for Multi 7+ building sub-types
    One list of energy efficiency values for Multi < 7 building sub-types
    :param building_efficiency_list: (list) a list of lists of [building sub-type, energy efficiency]
    :return: (list) a list of lists containing energy efficiency values for building sub-types of Multi 7+ and Multi < 7
    """
    # create empty lists to put the efficiency values into
    multi_7_plus = []
    multi_less_than_7 = []

    # go through each data tuple in energy_efficiency_list
    for item in building_efficiency_list:

        # if the building sub-type is Multi 7+
        if item[0] == "Multi 7+":

            # add its energy efficiency value to multi_7_plus
            multi_7_plus.append(item[1])

        # if the building sub-type is Multi < 7
        elif item[0] == "Multi < 7":
            # add its energy efficiency value to multi_less_than_7
            multi_less_than_7.append(item[1])

    # create a list of the energy efficiency lists
    efficiency_values_list = [multi_7_plus, multi_less_than_7]

    # return the list of lists of energy efficiency values
    return efficiency_values_list


def energy_efficiency_medians(efficiency_values_list):
    """
    Takes a list of lists of energy efficiency values and returns a list of their median values
    :param efficiency_values_list: (list) list of lists of energy efficiency values for each building sub-type
    :return: (list) a list that has 2 elements, the median energy efficiency of Multi 7+ and the median energy
    efficiency of Multi < 7 building types
    """
    # create a list to store the calculated avg values
    median_list = []

    # for each list of values in energy_efficiency list
    for lst in efficiency_values_list:

        # calculate the median of the list
        median_efficiency = median(lst)

        # append the median to median_list
        median_list.append(median_efficiency)

    # return the list of the two medians as [high-rise median, low-rise median]
    return median_list


def plot_high_and_low_rise(efficiency_values_list):
    """
    Takes a list of lists of efficiency values for high and low-rise multifamily buildings and makes box plots for each
    list
    :param efficiency_values_list: (list) a list of lists of efficiency values for high and low-rise multifamily
    buildings
    """
    values_7_plus = efficiency_values_list[0]
    values_less_than_7 = efficiency_values_list[1]

    # make a box plot of the values, do not show outliers
    box_plot_data = [values_less_than_7, values_7_plus]
    plt.boxplot(box_plot_data, showfliers = False, patch_artist = True, labels = ['Low-Rise', 'High-Rise'])

    # label the x and y axis
    plt.xlabel("Building Type")
    plt.ylabel("Energy Efficiency (KWH/sq feet)")

    # title the plot
    plt.title("Multi-Family Building Type v. Energy Efficiency in Chicago")

    # display the plot
    plt.savefig("visualization3.png")

    plt.show()


def main():
    """
    This function gets and prints the average KWH energy usage for winter and summer, and analyzes which season uses
    more energy
    :return: (none)
    """
    # *** QUESTION 1 *** #

    # Find the average data for winter and summer
    average_data_winter = average_season_kwh_data(4, 5, 15)
    average_data_summer = average_season_kwh_data(9, 10, 11)

    # Print results
    print("The average KWH used in Chicago during the winter months of December through February is: " + str(
        average_data_winter) + " KWH")
    print("The average KWH used in Chicago during the summer months of June through August is: " + str(
        average_data_summer) + " KWH")

    # Determine whether the energy usage is greater in the winter or summer
    if average_data_winter > average_data_summer:
        # find difference between data
        winter_minus_summer = average_data_winter - average_data_summer
        print("In the winter months, Chicago uses " + str(
            winter_minus_summer) + " more KWH of energy than in the summer months")
    elif average_data_winter < average_data_summer:
        # find difference between data
        summer_minus_winter = average_data_summer - average_data_winter
        print("In the summer months, Chicago uses " + str(
            summer_minus_winter) + " more KWH of energy than in the winter months")
    else:
        print("Chicago uses the same amount of energy during the winter and summer months")

    scatter_plot("b.")

    # *** QUESTION 2 *** #

    # assign which csvs are going to get analyzed
    income_data = parse_income_data("socioeconomic.csv")
    energy_data = parse_energy_data("energy-usage-2010.csv")

    # call correlate_data on the parsed income and energy data
    data = income_and_energy_correlate_data(income_data, energy_data)

    # calculate and print the correlation between income and energy
    spearman = spearman_income_and_energy(data)
    print("Spearman correlation for average community income and personal energy use:\n" + str(spearman))

    # plot the data
    plot_income_and_energy(data, 'b.')

    # *** QUESTION 3 *** #

    # get a list of
    building_data = parse_energy_for_apartments("energy-usage-2010.csv")

    # plot the data
    plot_high_and_low_rise(building_data)

    efficiency_stats = energy_efficiency_medians(building_data)

    print("Median energy efficiencies (KWH/sq ft):\nHigh-Rise: " + str(efficiency_stats[0]) + "\nLow-Rise: " + str(
        efficiency_stats[1]))
    print("High-rise apartments generally use " + str(
        efficiency_stats[1] - efficiency_stats[0]) + " less KWH/sq ft than low-rise apartments.")


if __name__ == '__main__':
    main()