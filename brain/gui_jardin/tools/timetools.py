class MyTime():
    """
    This class regroups useful tricks and small transforms that you may have to use when working with time and dates
    """

    def daytosec(days):
        """
        Pass in the number of days as INT and it will return the same amount of time expressed in seconds 
        """
        type(days) == int or raise TypeError

        # days * hours * min * sec
        return days * 24 * 60 * 60 

    def weektosec(week):
        return daytosec(7*week)


    def monthtosec(month):
        """
        Takes a number of (int) months as a parameter and returns the same amount of time expressed in seconds
        As we talk about plants, we approximate a month to be 30 days, this precision level is suffisant when talking about flowering or growing period.
        """
        return daytosec(30*month)



