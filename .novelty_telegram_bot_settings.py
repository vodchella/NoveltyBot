LOG_PATH = '/home/twister/Dropbox/novelty_utils/log'

SERVER_LOCAL_ADDRESS_MAIN = '192.168.1.119'
SERVER_LOCAL_ADDRESS_RESERVE = '192.168.1.118'
SERVER_LOCAL_ADDRESS_TEST = '192.168.1.122'
SERVER_LOCAL_ADDRESS_DB = '192.168.1.8'

DB_PASSWORD = 'inxJM3nm7ouu0'

SERVERS = [
    # Тестовые
    {
        'id': 'server_id_01',
        'name': 'Тестовый Аско',
        'subdomains': ['testasko'],
        'db': {
            'user_name': 'asko',
            'password': 'asko',
            'address': SERVER_LOCAL_ADDRESS_DB,
            'port': 1616,
            'service_name': 'test1'
        }
    },
    {
        'id': 'server_id_02',
        'name': 'Тестовый Евразия',
        'subdomains': ['testeur'],
        'db': {
            'user_name': 'eur',
            'password': 'eur',
            'address': SERVER_LOCAL_ADDRESS_DB,
            'port': 1616,
            'service_name': 'test1'
        }
    },
    {
        'id': 'server_id_03',
        'name': 'Тестовый Интертич',
        'subdomains': ['testinter'],
        'db': {
            'user_name': 'inter',
            'password': 'inter',
            'address': SERVER_LOCAL_ADDRESS_DB,
            'port': 1616,
            'service_name': 'test1'
        }
    },
    {
        'id': 'server_id_04',
        'name': 'Тестовый Компетенц',
        'subdomains': ['testkompetenz'],
        'db': {
            'user_name': 'allianz',
            'password': 'allianz',
            'address': SERVER_LOCAL_ADDRESS_DB,
            'port': 1616,
            'service_name': 'test1'
        }
    },
    {
        'id': 'server_id_05',
        'name': 'Тестовый Номад',
        'subdomains': ['testnomad'],
        'db': {
            'user_name': 'nomad',
            'password': 'nomad',
            'address': SERVER_LOCAL_ADDRESS_DB,
            'port': 1616,
            'service_name': 'test1'
        }
    },
    {
        'id': 'server_id_06',
        'name': 'Тестовый Нурполис',
        'subdomains': ['testnur'],
        'db': {
            'user_name': 'nur',
            'password': 'nur',
            'address': SERVER_LOCAL_ADDRESS_DB,
            'port': 1616,
            'service_name': 'test1'
        }
    },
    # Боевые
    {
        'id': 'server_id_07',
        'name': 'Аско',
        'subdomains': ['asko', 'asko2'],
        'db': {
            'user_name': 'pavlov_m[asko]',
            'password': DB_PASSWORD,
            'address': SERVER_LOCAL_ADDRESS_DB,
            'port': 1517,
            'service_name': 'nov_dev'
        }
    },
    {
        'id': 'server_id_08',
        'name': 'Евразия',
        'subdomains': ['eur', 'eur2'],
        'db': {
            'user_name': 'pavlov_m[eur]',
            'password': DB_PASSWORD,
            'address': SERVER_LOCAL_ADDRESS_DB,
            'port': 1517,
            'service_name': 'nov_dev'
        }
    },
    {
        'id': 'server_id_09',
        'name': 'Интертич',
        'subdomains': ['inter', 'inter2'],
        'db': {
            'user_name': 'pavlov_m[inter]',
            'password': DB_PASSWORD,
            'address': SERVER_LOCAL_ADDRESS_DB,
            'port': 1517,
            'service_name': 'nov_dev'
        }
    },
    {
        'id': 'server_id_10',
        'name': 'Компетенц',
        'subdomains': ['kompetenz', 'kompetenz2'],
        'db': {
            'user_name': 'pavlov_m[allianz]',
            'password': DB_PASSWORD,
            'address': SERVER_LOCAL_ADDRESS_DB,
            'port': 1517,
            'service_name': 'nov_dev'
        }
    },
    {
        'id': 'server_id_11',
        'name': 'Номад',
        'subdomains': ['nomad', 'nomad2'],
        'db': {
            'user_name': 'pavlov_m[nomad]',
            'password': DB_PASSWORD,
            'address': SERVER_LOCAL_ADDRESS_DB,
            'port': 1517,
            'service_name': 'nov_dev'
        }
    },
    {
        'id': 'server_id_12',
        'name': 'Нурполис',
        'subdomains': ['nur', 'nur2'],
        'db': {
            'user_name': 'pavlov_m[nur]',
            'password': DB_PASSWORD,
            'address': SERVER_LOCAL_ADDRESS_DB,
            'port': 1517,
            'service_name': 'nov_dev'
        }
    },
    {
        'id': 'server_id_13',
        'name': 'Novelty',
        'subdomains': ['home', 'home2'],
        'db': {
            'user_name': 'pavlov_m[home]',
            'password': DB_PASSWORD,
            'address': SERVER_LOCAL_ADDRESS_DB,
            'port': 1517,
            'service_name': 'nov_dev'
        }
    }
]

LOCAL_ADDRESSES = {
    'testasko': {
        'server': SERVER_LOCAL_ADDRESS_TEST,
        'jane_name': 'jane_asko'
    },
    'testeur': {
        'server': SERVER_LOCAL_ADDRESS_TEST,
        'jane_name': 'jane_eur'
    },
    'testinter': {
        'server': SERVER_LOCAL_ADDRESS_TEST,
        'jane_name': 'jane_inter'
    },
    'testkompetenz': {
        'server': SERVER_LOCAL_ADDRESS_TEST,
        'jane_name': 'jane_kompetenz'
    },
    'testnomad': {
        'server': SERVER_LOCAL_ADDRESS_TEST,
        'jane_name': 'jane_nomad'
    },
    'testnur': {
        'server': SERVER_LOCAL_ADDRESS_TEST,
        'jane_name': 'jane_nur'
    },
    'asko': {
        'server': SERVER_LOCAL_ADDRESS_MAIN,
        'jane_name': 'jane_asko'
    },
    'asko2': {
        'server': SERVER_LOCAL_ADDRESS_RESERVE,
        'jane_name': 'jane_asko'
    },
    'eur': {
        'server': SERVER_LOCAL_ADDRESS_MAIN,
        'jane_name': 'jane_eur'
    },
    'eur2': {
        'server': SERVER_LOCAL_ADDRESS_RESERVE,
        'jane_name': 'jane_eur'
    },
    'inter': {
        'server': SERVER_LOCAL_ADDRESS_MAIN,
        'jane_name': 'jane_inter'
    },
    'inter2': {
        'server': SERVER_LOCAL_ADDRESS_RESERVE,
        'jane_name': 'jane_inter'
    },
    'kompetenz': {
        'server': SERVER_LOCAL_ADDRESS_MAIN,
        'jane_name': 'jane_kompetenz'
    },
    'kompetenz2': {
        'server': SERVER_LOCAL_ADDRESS_RESERVE,
        'jane_name': 'jane_kompetenz'
    },
    'nomad': {
        'server': SERVER_LOCAL_ADDRESS_MAIN,
        'jane_name': 'jane_nomad'
    },
    'nomad2': {
        'server': SERVER_LOCAL_ADDRESS_RESERVE,
        'jane_name': 'jane_nomad'
    },
    'nur': {
        'server': SERVER_LOCAL_ADDRESS_MAIN,
        'jane_name': 'jane_nur'
    },
    'nur2': {
        'server': SERVER_LOCAL_ADDRESS_RESERVE,
        'jane_name': 'jane_nur'
    },
    'home': {
        'server': SERVER_LOCAL_ADDRESS_MAIN,
        'jane_name': 'jane_home'
    },
    'home2': {
        'server': SERVER_LOCAL_ADDRESS_RESERVE,
        'jane_name': 'jane_home'
    }
}
