import requests
import mammoth # type: ignore
from django.conf import settings
from .serializers import ForgejoUserPreCreSerializer, ForgejoUserCreateSerializer


def create_forgejo_user(kwargs: dict):
    ''' {
        created_at: date/time
        email*: string
        full_name: string
        login_name: string
        must_change_password: string
        password*: string
        restricted: boolean
        send_notify: boolean
        source_id: integer
        username*: string
        visibility: string
    } '''
    payload = kwargs.copy()
    response = requests.post(
                            url=f'{settings.FORGEJO_URL}/admin/users',
                            data=payload,
                            params={'token': settings.FORGEJO_TOKEN},
                            timeout=60)
    if response.status_code != 201:
        raise Exception(response.json())
    return response.json()


def get_forgejo_user(email: str):
    payload = {}
    username = email.split('@')[0]
    payload['token'] = settings.FORGEJO_TOKEN
    response = requests.get(
        # url=f'{settings.FORGEJO_URL}/admin/users',
        url=f'{settings.FORGEJO_URL}/users/{username}',
        params=payload,
        timeout=60
    )
    if response.status_code == 200:
        return response.json()
    raise Exception(response.json())


# def retrieve_forgejo_user(email: str):
#     data = get_forgejo_user({})
#     retrieved_user = {}
#     if data:
#         for user in data:
#             if user.get('email') == email:
#                 retrieved_user = user
#                 break
#     return retrieved_user


def delete_forgejo_user(username: str, purge=True):
    '''{
        username: string,
        purge: boolean
    }'''
    response = requests.delete(
        url=f'{settings.FORGEJO_URL}/admin/users/{username}',
        params={
            'purge': purge,
            'token': settings.FORGEJO_TOKEN},
        timeout=60
    )
    if response.status_code == 204:
        return None
    raise Exception(response.json())


def create_forgejo(data, user_id, *args, **kwargs):
    forgejo_serializer = ForgejoUserPreCreSerializer(data=data)
    if forgejo_serializer.is_valid():
        try:
            user_data = create_forgejo_user(forgejo_serializer.data)
        except Exception as e: raise
        
        user_data['user_id'] = user_id
        user_serializer = ForgejoUserCreateSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return user_serializer.data
        if user_data:
            delete_forgejo_user(username=user_data['username'], purge=True)
        raise Exception(user_serializer.errors)
    raise Exception(forgejo_serializer.errors)    
            

def create_forgejo_repo(username: str, data: dict):
    '''{
        auto_init: boolean
        default_branch: string
        description: string
        gitignores: string
        issue_labels: string
        license: string
        name: string (required)
        private: boolean
        readme: string
        template: boolean
        trust_model: string
    }'''
    response = requests.post(
        url=f'{settings.FORGEJO_URL}/admin/users/{username}/repos',
        params={'token': settings.FORGEJO_TOKEN},
        data=data
    )
    if response.status_code == 201:
        return response.json()
    raise Exception(response.json())


def get_forgejo_repo(username: str, repo: str):
    response = requests.get(
        url=f'{settings.FORGEJO_URL}/repos/{username}/{repo}',
        params={'token': settings.FORGEJO_TOKEN},
    )
    if response.status_code == 200:
        return response.json()
    raise Exception(response.json())


def upload_get_file_to_repo(
    username: str, repo: str, filepath: str, 
    data: dict={}, params:dict={}, method='GET') -> dict:
    """data = {
        author: {
            email: string
            name: string
        }
        branch: string
        committer: {
            email: string
            name: string
        }
        content: string (required)
        dates: {
            author: string
            committer: string
        }
        message: string
        new_branch:	string
        signoff: boolean
    }
    """
    url = f'{settings.FORGEJO_URL}/repos/{username}/{repo}/contents/{filepath}'
    payload = params.copy()
    payload['token'] = settings.FORGEJO_TOKEN
    response = None
    if method.lower() == 'post':
        response = requests.post(
            url=url,
            params=payload,
            json=data
        )
    elif method.lower() == 'put':
        response = requests.put(
            url=url,
            params=payload,
            json=data
        )
    elif method.lower() == 'get':
        response = requests.get(
            url=url,
            params=payload,
        )
        
    if response.status_code in [200, 201]:
        return response.json()
    raise Exception(response.json().get('message', 'Not Found'))


def docx_to_html(path: str) -> dict:
    response = {}
    
    with open(path,'rb') as docx_file:
        result = mammoth.convert_to_html(docx_file)
        response['data'] = result.value
    return response
