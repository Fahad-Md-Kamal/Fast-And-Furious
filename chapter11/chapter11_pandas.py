import pandas as pd

# paid = {"Louvre Museum": 5988065, "Orsay Museum": 1850092, "Pompidou Center": 2620481, "National Natural History Museum": 404497}
# free = {"Louvre Museum": 4117897, "Orsay Museum": 1436132, "Pompidou Center": 1070337, "National Natural History Museum": 344572}

# museums = pd.DataFrame({"paid": paid, "free": free})
museums = pd.read_csv("./museums.csv", index_col=0)

