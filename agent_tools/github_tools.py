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

    def get_single_repository_contents(self) -> None:

        try:

            repository: Repository = self._github_object.get_repo("hsr205/Reinforcement-Learning-Trading-Agent")

            repository_content: list[ContentFile] | ContentFile = repository.get_contents("models/")

            if isinstance(repository_content, ContentFile):
                content_file: ContentFile = repository_content
                self._logger.info(content_file.decoded_content.decode("utf-8"))

            elif isinstance(repository_content, list):
                content_list: list[ContentFile] = repository_content

                for element in content_list:
                    if "__" in element.name:
                        continue
                    self._logger.info(f"File Name: {element.name}")
                    self._logger.info("=" * 100)
                    self._logger.info(element.decoded_content.decode("utf-8"))
                    self._logger.info("=" * 100)

        except Exception as e:
            self._logger.error(f"Exception Thrown: {e}")
            raise Exception
