from github import Auth
from github import Github
from github.ContentFile import ContentFile
from github.Repository import Repository

from config.config import Settings
from logger.logger import AppLogger


class GithubTools:

    def __init__(self) -> None:
        self._config: Settings = Settings()
        self._auth = Auth.Token(token=self._config.github_access_token)
        self._github_object: Github = Github(auth=self._auth)
        self._logger = AppLogger.get_logger(self.__class__.__name__)

    def display_all_repository_names(self) -> None:

        try:

            for repo in self._github_object.get_user().get_repos():
                self._logger.info(f"repo = {repo.full_name}")

        except Exception as e:
            self._logger.error(f"Exception Thrown: {e}")
            raise Exception

    def get_single_repository_file_contents(self,
                                            repository_name_str: str = "hsr205/Reinforcement-Learning-Trading-Agent",
                                            file_name: str = "README.md") -> str:

        try:

            repository: Repository = self._github_object.get_repo(full_name_or_id=repository_name_str)

            repository_content: list[ContentFile] | ContentFile = repository.get_contents(file_name)

            if isinstance(repository_content, ContentFile):
                content_file: ContentFile = repository_content
                file_contents: str = content_file.decoded_content.decode("utf-8")
                return file_contents

        except Exception as e:
            self._logger.error(f"Exception Thrown: {e}")
            raise Exception

    def get_single_repository_directory_file_contents_dict(self,
                                                      repository_name_str: str = "hsr205/Reinforcement-Learning-Trading-Agent",
                                                      directory_name_str: str = "models") -> dict[str,str]:

        result_dict:dict[str,str] = {}

        try:

            repository: Repository = self._github_object.get_repo(full_name_or_id=repository_name_str)

            repository_content: list[ContentFile] | ContentFile = repository.get_contents(path=directory_name_str)

            if isinstance(repository_content, list):
                content_list: list[ContentFile] = repository_content

                for file_content in content_list:

                    file_name_str:str = file_content.name

                    if "__" in file_name_str:
                        continue

                    file_contents: str = file_content.decoded_content.decode("utf-8")

                    result_dict[file_name_str] = file_contents

            return result_dict

        except Exception as e:
            self._logger.error(f"Exception Thrown: {e}")
            raise Exception
