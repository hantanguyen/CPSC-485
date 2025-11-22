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
    dp_matrix = [[0] * (n + 1) for i in range(m + 1)]

    # We need the minimum edits to turn word1 into an empty string since its a specific case for the word a user can enter
    # EX : word1 = "dog" -> dp[3][0] = 3(delete 'd','o','g')
    # Start the first column since we need to turn word1 into an empty string
    for i in range(m + 1):
        # i deletions needed 
        dp_matrix[i][0] = i

    # We need the minimum edits to turn the empty string into word2 
    # EX: word2 = "dog" -> dp[0][3] = 3(insert 'd','o','g')
    # Start with the first row 
    for j in range(n + 1): 
        # j insertions needed 
        dp_matrix[0][j] = j

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

            dp_matrix[i][j] = min(
                # Insert a character
                dp_matrix[i][j - 1] + 1,  
                # Delete a character
                dp_matrix[i - 1][j] + 1, 
                # Substitute a character
                dp_matrix[i - 1][j - 1] + substitute_cost
            )
    # return dp table 
    return dp_matrix

# Implement the alignment function where the two strings of word1 and word2 will show the edits if there was a match, insertion, deletion, or substitution 
# This function will need to take 3 parameters, word1, word2, dp_matrix
def alignment(word1, word2, dp_matrix,):

    # starts at the end of word1, decrement i when a character is used from word1
    i = len(word1)
     # starts at the end of word2, decrement j when a character is used from word2
    j = len(word2)

    # empty to build the top alignment using characters from word1 like "_" for the gaps
    top_alignment = ""
    # empty to build the bottom alignment using characters from word2 like "_" for the gaps
    bottom_alignment = "" 

    # Start to loop through both words, stop when i == 0 and j == 0 
    while i > 0 or j > 0: 
        # for a diagonal operation(match or substitute) and if both words still have characters 
        if i > 0 and j > 0: 
            # compare the last character of each word and if they match then the cost is 0 
            # but if we need to substitute then it'll cost 1 
            if word1[i - 1] == word2[j - 1]:
                substitute_cost = 0 
            else: 
                substitute_cost = 1

            # check to see if the minimum cost was diagonal from dp_matrix[i-1][j-1] and if it was a match or a substitute(costs less compared to an insertion or deletion)
            if dp_matrix[i][j] == dp_matrix[i - 1][j - 1] + substitute_cost: 
            # this also means that the best move was a diagonal move 
                # put the current character from word1 at the front of the top alignment string 
                top_alignment = word1[i - 1] + top_alignment
                # put the current character from word2 at the front of the bottom alignment string 
                bottom_alignment = word2[j - 1] + bottom_alignment
                # decrement one character back from word1 
                i -= 1
                # decrement one character back from word2
                j -= 1
                # continue since this is only considering if we make a diagonal move not up or left in the table 
                continue 
        
        # if we deleted the last character of word1
        if i > 0 and dp_matrix[i][j] == dp_matrix[i - 1][j] + 1:
            # add deleted character from word1 to the top_alignment 
            top_alignment = word1[i - 1] + top_alignment
            # add a "_" to the bottom_alignment since there wasn't a character from word2 that lined up with the position of word1
            bottom_alignment = "_" + bottom_alignment
            # move through the dp_matrix
            i -= 1
            # continue since this is only considering if we deleted any characters 
            continue

        # if we came from the left insertion of word2
        if j > 0 and dp_matrix[i][j] == dp_matrix[i][j - 1] + 1: 
            # add a "_" to the top_alignment since there wasn't a character that matched from word1 
            top_alignment = "_" + top_alignment
            # add inserted character from word2 to the bottom_alignment 
            bottom_alignment = word2[j - 1] + bottom_alignment
            # move left through the dp_matrix
            j -= 1
            # continue since this is only considering if we moved any characters 
            continue

    return top_alignment, bottom_alignment

# Flask Routing 
@app.route("/", methods=["GET", "POST"])
def index():

    dp_matrix = None
    distance = None
    top_alignment = ""
    bottom_alignment = ""
    word1 = ""
    word2 = ""

    if request.method == "POST":
        word1 = request.form.get("word1", "")
        word2 = request.form.get("word2", "")

        dp_matrix = edit_distance_algorithm(word1, word2)
        distance = dp_matrix[len(word1)][len(word2)]
        top_alignment, bottom_alignment = alignment(word1, word2, dp_matrix)

    return render_template(
        "index.html",
        matrix=dp_matrix,
        distance=distance,
        top_alignment=top_alignment,
        bottom_alignment=bottom_alignment,
        word1=word1,
        word2=word2
    )


if __name__ == "__main__":
    app.run(debug=True)
