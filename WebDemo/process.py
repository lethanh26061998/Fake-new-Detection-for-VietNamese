import sys 

# print("Output from Python") 
# print("First name: " + sys.argv[1]) 
# print("Last name: " + sys.argv[2])

def simulate(message, timestamp):
    predic_result = "YES"
    results = {
        'message': message,
        'timestamp': timestamp,
        'result' : predic_result
    }
    return results