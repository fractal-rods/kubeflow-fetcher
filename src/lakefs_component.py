from src.lakefs_client import login_to_lakefs, get_data, post_data


def lakefs_test_client(host, username, password):
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


if __name__ == "__main__":
    lakefs_test_client()

    # comp.create_component_from_func(
    #    func=lakefs_test_client,
    #    base_image="python:3.10-alpine",
    #    packages_to_install="requests",
    #    output_component_file="lakefs-demo-component",
    #    )
