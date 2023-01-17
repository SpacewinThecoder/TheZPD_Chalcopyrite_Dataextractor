import json


def main():
    data_0 = []
    data = []
    with open('result_0.json', 'r') as f:
        data_0 = json.load(f)
    with open('result.json', 'r') as f:
        data = json.load(f)
    print(f'{len(data_0)=}')
    print(f'{len(data)=}')


if __name__ == '__main__':
    main()
