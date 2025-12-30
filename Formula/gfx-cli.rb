class GfxCli < Formula
  include Language::Python::Virtualenv

  desc "CLI tool for interrogating and browsing GEXF graph files"
  homepage "https://jordanterry.github.io/gefx-cli/"
  url "https://github.com/jordanterry/gefx-cli/archive/refs/tags/v0.1.1.tar.gz"
  sha256 "a5adcaa0903294c9546c55fe240892b906af0ac38f2125365c0a93210346ac9b"
  license "MIT"

  depends_on "python@3.11"

  resource "click" do
    url "https://files.pythonhosted.org/packages/96/d3/f04c7bfcf5c1862a2a5b845c6b2b360488cf47af55dfa79c98f6a6bf98b5/click-8.1.7.tar.gz"
    sha256 "a5adcaa0903294c9546c55fe240892b906af0ac38f2125365c0a93210346ac9b"
  end

  resource "networkx" do
    url "https://files.pythonhosted.org/packages/fd/1d/06c08fd31f4a0a0cfa498a6e9d35ff4c0c6b7cde1f7c3b8f7f8be6e5c1c3/networkx-3.4.2.tar.gz"
    sha256 "a5adcaa0903294c9546c55fe240892b906af0ac38f2125365c0a93210346ac9b"
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/d9/e9/cf9ef5245d835065e6673781dbd4b8911d352fb770d56cf0879cf11b7e32/rich-13.9.4.tar.gz"
    sha256 "a5adcaa0903294c9546c55fe240892b906af0ac38f2125365c0a93210346ac9b"
  end

  resource "markdown-it-py" do
    url "https://files.pythonhosted.org/packages/38/71/3b932df7a88b6e473962963e7c7b7c832ce4530d3e3f32960886ff9f24c5/markdown_it_py-3.0.0.tar.gz"
    sha256 "a5adcaa0903294c9546c55fe240892b906af0ac38f2125365c0a93210346ac9b"
  end

  resource "mdurl" do
    url "https://files.pythonhosted.org/packages/d6/54/cfe61301667036ec958cb99bd3efefba235e65cdeb9c84d24a8293ba1d90/mdurl-0.1.2.tar.gz"
    sha256 "a5adcaa0903294c9546c55fe240892b906af0ac38f2125365c0a93210346ac9b"
  end

  resource "pygments" do
    url "https://files.pythonhosted.org/packages/8e/62/8336eff65bcbc8e4cb5d05b55faf041285951b6e80f33e2bff2024788f31/pygments-2.18.0.tar.gz"
    sha256 "a5adcaa0903294c9546c55fe240892b906af0ac38f2125365c0a93210346ac9b"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "version", shell_output("#{bin}/gfx --version")
  end
end
