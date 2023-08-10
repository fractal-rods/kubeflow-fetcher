from client import login_to_lakefs, get_data, post_data
import argparse
import os


def modify_lake_data(host, id, token):
    os.environ.update(LAKEFS_HOST=host, LAKEFS_ID=id, LAKEFS_TOKEN=token)

    # 1.Login
    token = login_to_lakefs()

    # 2.Get data from response and modify it
    response = get_data(token)
    data = response.text
    print("data: " + data)

    data += " ...new data here also"
    print("updated data: " + data)

    # 3.Write the data into a file and send to lakefs
    with open("model.txt", "w") as file:
        file.write(data)

    post_data(token)


parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, help="lakefs host address")
parser.add_argument("--id", type=str, help="lakefs access id")
parser.add_argument("--token", type=str, help="lakefs secret token")
args = parser.parse_args()

modify_lake_data(host=args.host, id=args.id, token=args.token)
