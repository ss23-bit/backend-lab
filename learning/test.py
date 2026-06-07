emails = [
    "a@test.com",
    "b@test.com",
    "a@test.com"
]

seen = set()
duplicates = []

for email in emails:
    if email not in seen:
        seen.add(email)
    else:
        duplicates.append(email)
print(duplicates)
    
