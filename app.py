# Importing Flask(main framework), render template(loading HTML files), and request(reading the input from user)
from flask import Flask, render_template, request

# Make the Flask app 
app = Flask(__name__)

# Implementing edit distance algorithm function that takes two parameters, word1 and word2
def edit_distance_algorithm(word1, word2):
    
    # Get the lengths of word1 and word2 
    m, n = len(word1), len(word2)

    # creating the dynamic programming (dp) matrix where (m + 1) x (n + 1) are filled with 0's
    # Use a list comprehension here since it makes a matrix with m + 1 rows and n + 1 columns that make a new n + 1 0's for each row 
    dp = [[0] * (n + 1) for i in range(m + 1)]

    # We need the minimum edits to turn word1 into an empty string since its a specific case for the word a user can enter
    # EX : word1 = "dog" -> dp[3][0] = 3(delete 'd','o','g')
    # Start the first column since we need to turn word1 into an empty string
    for i in range(m + 1):
        # i deletions needed 
        dp[i][0] = i

    # We need the minimum edits to turn the empty string into word2 
    # EX: word2 = "dog" -> dp[0][3] = 3(insert 'd','o','g')
    # Start with the first row 
    for j in range(n + 1): 
        # j insertions needed 
        dp[0][j] = j

    # These are the base cases the DP uses to compute all other cells in the matrix 

    # Now we need to fill in the rest of the matrix 
    # Using a nested for loop we iterate through thr length of each of the words
    for i in range(1, m + 1): 
        for j in range(1, n + 1):
            # if one of the characters match, then the cost of the operation is 0 
            # but insertion, deletion, and substitution will cost 1
            if word1[i - 1] == word2[j - 1]: 
                # match is 0 cost 
                substitute_cost = 0 
            else: 
                # if it isn't a match then it cost 1 
                substitute_cost = 1

            # now we need to find the minimum cost to turn word1[:i] into word2[:j] 

            """ Operations: 
            1. Insert a character 
            (i, j + 1)
            2. Delete a character
            (i + 1, j)
            3. Substitute a character
            (i + 1, j + 1)
            """

            dp[i][j] = min(
                # Insert a character
                dp[i][j - 1] + 1,  
                # Delete a character
                dp[i - 1][j] + 1, 
                # Substitute a character
                dp[i - 1][j - 1] + substitute_cost
            )
    # return dp table 
    return dp 
