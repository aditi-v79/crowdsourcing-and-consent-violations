# crowdsourcing-and-consent-violations
--This project takes 64 excel workbooks as input. Each excel workbook consists of 2500 reviews on different apps and the atmost 3 labels of consent violations assigned by the crowd worker( to whom the workbook belongs to).
--This project effectively combines all the crowdsourced data, detect the fake files(using Cohen's kappa) and assigns the final labels based on the majority voting from the 64 crowd worker inputs.

README:
a) Please install the libraries in the import statements in those python files if necessary, apart from the below commands
b) Make sure the "P2a Labels" folder and the Python files are in the same location while trying to run the Python files.


Note: - Few Python files may generate .csv files(just for reference of the output)
      - Files 50.xlsx was excluded from this project.
      - File 15.xlsx was modified by removing the explainations for this assignment.
 

-->File: crowdsourcing_reviews.py

1) Commands to install necessary libraries:
	-- pip install pandas

2) Run the program ( make sure you are inside the folder where the crowdsourcing_reviews.py):
	-- python .\crowdsourcing_review.py


-->File: detect_fakefiles.py

1) Install necessary libraries:
	-- pip install scikit-learn

2) Run the program ( make sure you are inside the folder where the detect_fakefiles.py):
	-- python .\detect_fakefiles.py

-->File: majority_voting.py

1)  Install necessary libraries:
	-- pip install wordcloud
	-- pip install nltk
	-- pip install matplotlib

2) Run the program ( make sure you are inside the folder where the majority_reviews.py):
	-- python .\majority_reviews.py



