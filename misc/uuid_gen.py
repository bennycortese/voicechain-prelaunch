import uuid
import json

# Generate 100 UUIDs
uuid_list = ["invite-" + str(uuid.uuid4()) for _ in range(100)]

# Create a dictionary with each invite code mapped to 0
invite_codes = {uuid: 0 for uuid in uuid_list}

# Write the dictionary to a JSON file
with open("invite_codes.json", "w") as file:
    json.dump(invite_codes, file, indent=4)

print("Invite codes have been written to invite_codes.json")
