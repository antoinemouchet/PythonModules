import json


class NoCreditException(Exception):
    """
    Exception when no course considerated
    """
    pass


def get_credits_info(file_path="Results2.json"):
    """
    Returns the number of credits written in the file  indicated by the file_path
    even if no note is indicated for a course

    Parameters
    ----------
    file_path: path of the json file with notes, courses and credits (str)

    Returns
    -------
    credit_list: [credits of courses with a note, credits of courses without, total amount] (list of int)

    Note
    -----
    The json file should have elements with
    {"name":string, "credits": int, "note": float} format

    """
    credit_list = [0, 0, 0]

    results = json.load(open(file_path))

    for result in results:

        course_credit = result["credits"]

        if(result["note"] != "NA"):
            # Number of credits of course with a note 
            credit_list[0] += course_credit
        else:
            # Number of credits of course without a note
            credit_list[1] += course_credit

        credit_list[2] += course_credit

    return credit_list



def get_mean(file_path="Results2.json"):
    """
    Returns the weighted arithmetic mean of the notes of each course specified
    in the json file
    indicated by the file_path and the amount of credits considered
    for this mean.

    Parameters
    ----------
    file_path: path of the json file with notes, courses and credits (str)

    Returns
    -------
    mean: weighted arithmetic mean of the notes by the credits
    of each course (float)
    nb_credits: total number of credits considered (int)

    Note
    -----
    The json file should have elements with
    {"name":string, "credits": int, "note": float} format

    """
    mean = 0
    nb_credits = 0

    results = json.load(open(file_path))

    for result in results:
        # Get note of course
        note = result["note"]

        if(note != "NA"):
            # Get nb Credits of class
            ponderation = result["credits"]

            # Add ponderated note to mean
            mean += (ponderation * note)
            # Add nb of credit of the course to total nb of credits
            nb_credits += ponderation

    # Avoid / by 0
    if nb_credits == 0:
        raise NoCreditException

    # Get actual mean
    mean /= nb_credits
    return mean, nb_credits


def get_mean_stats(file_path="Results2.json"):
    """
    Returns the weighted arithmetic mean of the notes of each course
    specified in the json file indicated by the file_path,
    the amount of credits considered for this mean and some other stats.

    Parameters
    ----------
    file_path: path of the json file with notes, courses and credits (str)

    Returns
    -------
    mean: weighted arithmetic mean of the notes by the credits
    of each course (float)
    nb_credits: total number of credits considered (int)
    low: lowest note (float)
    high: highest note (float)
    low_name: name of the course with lowest note (string)
    high_name: name of the course with highest note (string)

    Note
    -----
    The json file should have elements with
    {"name":string, "credits": int, "note": float} format

    """
    # File with results
    results = json.load(open(file_path))

    # Initialize some values
    low = 20
    high = 0
    mean = 0
    nb_credits = 0

    for result in results:
        # Get note of course
        note = result["note"]

        if(note != "NA"):
            # Check if note is new lowest
            if(note < low):
                low = note
                low_name = result["name"]

            # Check if note is new highest
            if(note > high):
                high = note
                high_name = result["name"]

            # Get nb Credits of class
            ponderation = result["credits"]

            # Add ponderated note to mean
            mean += (ponderation * note)
            # Add nb of credit of the course to total nb of credits
            nb_credits += ponderation

    if nb_credits == 0:
        raise NoCreditException

    # Get actual mean
    mean /= nb_credits

    return mean, nb_credits, low, high, low_name, high_name


def format_answer(mean, nb_credits, stats=False, low=0, high=0,
                  low_name="", high_name="", credits_info=False,
                  credits_valued=0, credits_not_valued=0, credits_file=0):
    """
    Returns a formatted string with the information computed.

    Parameters
    ----------
    mean: weighted arithmetic mean of the notes by the credits
    of each course (float)
    nb_credits: total number of credits considered (int)
    stats: statistics included? (bool)
    low: lowest note (float)
    high: highest note (float)
    low_name: name of the course with lowest note (string)
    high_name: name of the course with highest note (string)
    credits_info: credits info included ? (bool)
    credits_valued: number of credits with a note (int)
    credits_not_valued: number of credits without a note (int)
    credits_file: number of credits in the file (int)


    Return
    ------
    answer: the formatted string (str)

    Note
    ----
    if stats is at True then the following parameters should be given
    to the function
    """
    answer = "\n|---------------------------------------------|\n"
    answer += "|Moyenne de %.2f pour %d crédits considérés.|" %\
        (mean, nb_credits)
    answer += "\n|---------------------------------------------|\n"

    if stats:
        answer += "\n• Meilleure note: %.2f \t(%s)" % (high, high_name)
        answer += "\n• Moins bonne note: %.2f \t(%s)\n" % (low, low_name)

    if credits_info:
        answer += "\n• Nombre  de crédits dans le fichier: %d" % credits_file
        answer += "\n• Nombre de crédits déjà notés: %d" % credits_valued
        answer += "\n• Nombre de crédits restant: %d\n" % credits_not_valued

    return answer


def main():
    """
    Main function displays the most complete information
    """
    try:
        results = get_mean_stats()
        credits_stats = get_credits_info()

    except NoCreditException:
        print("No course considered. Make sure the Results.json file\
            is correctly configured.")
        return

    print(format_answer(results[0], results[1], True, results[2], results[3],
          results[4], results[5], True, credits_stats[0], credits_stats[1],
          credits_stats[2]))

if __name__ == "__main__":
    main()
