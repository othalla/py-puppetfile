import pytest

from control_repository.exceptions import (ModuleParserException,
                                           ModuleMalformedException)
from control_repository.modules import GitModule, ForgeModule


class TestGitModule:
    @staticmethod
    def test_with_unknow_reference():
        with pytest.raises(AttributeError):
            GitModule('nginx', 'https://url/repo/nginx.git', 'bad_reference',
                      'version')

    @staticmethod
    def test_if_module_has_reference_type_without_reference():
        with pytest.raises(ModuleMalformedException):
            GitModule('nginx',
                      'https://url/repo/nginx.git',
                      reference_type='branch')


class TestGitModuleFromLines:
    @staticmethod
    def test_it_returns_git_module_without_any_reference_type():
        git_module = GitModule.from_lines(
            ["mod 'apache',",
             "    :git => 'https://github.com/puppet/apache'",
             ])
        assert git_module.name == 'apache'
        assert git_module.git_url == 'https://github.com/puppet/apache'
        assert git_module.reference_type is None
        assert git_module.reference is None

    @staticmethod
    def test_with_ref_reference_type_returns_git_module():
        git_module = GitModule.from_lines(
            ["mod 'apache',",
             "    :git => 'https://github.com/puppet/apache'",
             "    :ref => '0adqs1'",
             ])
        assert git_module.name == 'apache'
        assert git_module.git_url == 'https://github.com/puppet/apache'
        assert git_module.reference_type == 'ref'
        assert git_module.reference == '0adqs1'

    @staticmethod
    def test_with_branch_reference_type_returns_git_module():
        git_module = GitModule.from_lines(
            ["mod 'apache',",
             "    :git    => 'https://github.com/puppet/apache'",
             "    :branch => 'branchname'",
             ])
        assert git_module.name == 'apache'
        assert git_module.git_url == 'https://github.com/puppet/apache'
        assert git_module.reference_type == 'branch'
        assert git_module.reference == 'branchname'

    @staticmethod
    def test_with_tag_reference_type_returns_git_module():
        git_module = GitModule.from_lines(
            ["mod 'apache',",
             "    :git => 'https://github.com/puppet/apache'",
             "    :tag => '0.1.1'",
             ])
        assert git_module.name == 'apache'
        assert git_module.git_url == 'https://github.com/puppet/apache'
        assert git_module.reference_type == 'tag'
        assert git_module.reference == '0.1.1'

    @staticmethod
    def test_with_commit_reference_type_returns_git_module():
        git_module = GitModule.from_lines(
            ["mod 'apache',",
             "    :git    => 'https://github.com/puppet/apache'",
             "    :commit => '0dfa12'",
             ])
        assert git_module.name == 'apache'
        assert git_module.git_url == 'https://github.com/puppet/apache'
        assert git_module.reference_type == 'commit'
        assert git_module.reference == '0dfa12'

    @staticmethod
    def test_with_missing_git_url():
        with pytest.raises(ModuleParserException):
            GitModule.from_lines(
                ["mod 'apache',",
                 "    :commit => '0dfa12'",
                 ])


class TestGitModuleToString:
    @staticmethod
    def test_it_convert_a_git_module_with_references_to_string():
        git_module = GitModule('apache',
                               'https://url/to/git/apache',
                               reference_type='branch',
                               reference='test')
        assert str(git_module) == ("mod 'apache',\n"
                                   "  :git => 'https://url/to/git/apache',\n"
                                   "  :branch => 'test'\n")

    @staticmethod
    def test_it_convert_a_git_module_without_reference_to_string():
        git_module = GitModule('apache', 'https://url/to/git/apache')
        assert str(git_module) == ("mod 'apache',\n"
                                   "  :git => 'https://url/to/git/apache'\n")


class TestGitModuleSetReference:
    @staticmethod
    def test_it_change_git_module_reference():
        git_module = GitModule('apache',
                               'https://url/to/git/apache',
                               reference_type='branch',
                               reference='test')
        assert git_module.reference == 'test'
        git_module.set_reference('newtest')
        assert git_module.reference == 'newtest'

    @staticmethod
    def test_it_update_both_reference_and_reference_type_if_supplied():
        git_module = GitModule('apache',
                               'https://url/to/git/apache',
                               reference_type='branch',
                               reference='test')
        assert git_module.reference == 'test'
        assert git_module.reference_type == 'branch'
        git_module.set_reference('1.0.0', reference_type='tag')
        assert git_module.reference == '1.0.0'
        assert git_module.reference_type == 'tag'


class TestForgeModuleToString:
    @staticmethod
    def test_it_convert_a_module_with_version_to_string():
        forge_module = ForgeModule('puppetlabs/apache', version='0.1.10')
        assert str(forge_module) == "mod 'puppetlabs/apache', '0.1.10'\n"

    @staticmethod
    def test_it_convert_a_module_without_version_to_string():
        forge_module = ForgeModule('puppetlabs/apache')
        assert str(forge_module) == "mod 'puppetlabs/apache'\n"


class TestForgeModuleSetVersion:
    @staticmethod
    def test_it_change_module_version():
        forge_module = ForgeModule('puppetlabs/apache', version='0.1.10')
        assert forge_module.version == '0.1.10'
        forge_module.set_version('0.1.11')
        assert forge_module.version == '0.1.11'


class TestForgeModuleFromLine:
    @staticmethod
    def test_it_returns_forge_module_from_line_without_version():
        forge_module = ForgeModule.from_line("mod 'puppetlabs/apache'")
        assert forge_module.name == 'puppetlabs/apache'
        assert forge_module.version is None

    @staticmethod
    def test_it_returns_forge_module_from_line_with_version():
        forge_module = ForgeModule.from_line("mod 'puppetlabs/apache', '0.1.1'")
        assert forge_module.name == 'puppetlabs/apache'
        assert forge_module.version == '0.1.1'

    @staticmethod
    def test_it_returns_forge_module_from_line_with_version_latest():
        forge_module = ForgeModule.from_line("mod 'puppetlabs/apache', :latest")
        assert forge_module.name == 'puppetlabs/apache'
        assert forge_module.version == ':latest'

    @staticmethod
    def test_with_a_bad_module():
        with pytest.raises(ModuleParserException):
            ForgeModule.from_line("mod 'puppetlabs/apache', '0.1', 'bad'")
