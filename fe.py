import random
import pandas as pd
import os

class SimpleScalarFE:
    def __init__(self):
        self.s = random.randint(2, 20)   # Master Secret Key
        self.p = 1000003
        self.y = random.randint(2, 10)   # Function (f(x) = yx)

    def encrypt(self, x):
        r = random.randint(2, 20)
        c1 = (x + r * self.s) % self.p
        c2 = r
        return (c1, c2)

    def keygen(self):
        return (self.s * self.y) % self.p

    def evaluate(self, cipher, key):
        c1, c2 = cipher
        return (c1 * self.y - c2 * key) % self.p


# ---------------- MAIN ---------------- #

# Step 1: Take input
x = int(input("Enter your data: "))

# Step 2: Initialize FE system
fe = SimpleScalarFE()

# Step 3: Encrypt
cipher = fe.encrypt(x)

# Step 4: Key generation
key = fe.keygen()

# Step 5: Functional computation
result = fe.evaluate(cipher, key)

# ---------------- SECRET SHARING (MPC STEP 1) ---------------- #

def generate_shares(y, num_parties=2):
    shares = []
    
    for _ in range(num_parties - 1):
        share = random.randint(-100, 100)
        shares.append(share)
    
    last_share = y - sum(shares)
    shares.append(last_share)
    
    return shares

shares = generate_shares(result, 4)

print("\n🔐 Shares Distributed:")
for i, s in enumerate(shares):
    print(f"Party {i+1} Share: {s}")

# ---------------- SAVE TO EXCEL ---------------- #

file_name = "fe_database.xlsx"

data = {
    "Input (x)": [x],
    "Function": [f"f(x) = {fe.y}x"],
    "Multiplier (y)": [fe.y],
    "Ciphertext c1": [cipher[0]],
    "Ciphertext c2": [cipher[1]],
    "Master Secret Key (s)": [fe.s],
    "Functional Key (SK)": [key],
    "Functional Output f(x)": [result],
    "Party 1 Share": [shares[0]],
    "Party 2 Share": [shares[1]],
    "Party 3 Share": [shares[2]],
    "Party 4 Share": [shares[3]]
}

assert sum(shares) == result, "Error in share generation!"

df_new = pd.DataFrame(data)

# Append if file exists
if os.path.exists(file_name):
    df_existing = pd.read_excel(file_name)
    df_final = pd.concat([df_existing, df_new], ignore_index=True)
else:
    df_final = df_new

df_final.to_excel(file_name, index=False)

# ---------------- USER OUTPUT ---------------- #

print("✅ Database updated")