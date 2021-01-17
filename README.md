# PythonStuff

In this repository you will find a lot of random stuff I do using Python.
Each functionality is in a distinct folder. You need to be in the corresponding directory to make it work.

## Moyenne

Script to compute the weighted arithmetic mean of courses with each weight being the number of credits for the course.

### How to use?

1. Fill in the ```Results.json``` file with your result for each course.
2. You can add all the courses you want as long as each course is a distinct JSON object following the format ```{"name": string, "credits": int, "note": float}```
3. Execute the following command:
```cmd
python main.py
```

If you do not want to take a course into consideration for the mean just set the "note" field of the JSON for the corresponding course to "NA".


## RandomQuote

Script to learn the use of a web scrapper. (Found on Internet)

### How to use?

1. Execute the following command:
```cmd
python main.py
```

## POO_Example

Script to get a bit more familiar with Object Oriented Programming in Python . (Found on Internet)

### How to use?

1. Execute the following command:
```cmd
python model.py
```

