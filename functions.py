
def filtering(list, prefix: tuple) -> list:
        """
        give a list of strings and a tuple of prefix, filtered the list
        by items started with prefix
        """
        filtered_loads = filter(lambda x:  x.startswith(prefix), list)
        return filtered_loads
