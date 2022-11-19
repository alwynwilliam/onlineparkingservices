import json

file_name = "db.json"
with open(file_name, "r") as file:
    data = json.load(file)


def get_destination(data):
    destinations = []
    for item in data:
        if item["model"] == "core.destinationmodel":
            destinations.append(item)

    return destinations


destinations = get_destination(data)


def create_destination(
    id, name, location, image, description, user, slot, created_on, updated_on
):
    destination = {
        "model": "core.destinationmodel",
        "pk": id,
        "fields": {
            "name": name,
            "location": location,
            "image": image,
            "description": description,
            "user": user,
            "status": True,
            "slots": slot,
            "created_on": created_on,
            "updated_on": updated_on,
        },
    }

    """
    {
    "model": "core.destinationmodel",
    "pk": 1,
    "fields": {
      "status": true,
      "created_on": "2022-11-17T12:43:50.689Z",
      "updated_on": "2022-11-17T12:43:50.689Z",
      "name": "Edakochi",
      "description": "Some Description",
      "location": null,
      "created_by": 1,
      "image": [1],
      "slots": [1]
    }
  }
    """
    return destination


destinations_new = []

for i, d in enumerate(destinations, start=2):
    file = d["fields"]["image"]
    image = {
        "model": "core.imagemodel",
        "pk": i,
        "fields": {"file": file},
    }
    destinations_new.append(image)
    name = d["fields"]["name"]
    description = "No description.."
    location = None
    dest = create_destination(
        id=i,
        name=name,
        location=location,
        image=[i],
        description=description,
        user=1,
        slot=[1],
        created_on="2022-11-10T13:11:13.755Z",
        updated_on="2022-11-10T13:11:13.755Z",
    )

    destinations_new.append(dest)

with open("db_new.json", "w", newline="") as file:
    destinations = json.dump(destinations_new, file, indent=4, sort_keys=True)

print(destinations)
