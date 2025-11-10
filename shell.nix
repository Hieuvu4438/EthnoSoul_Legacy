{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.poppler_utils  # Tools: pdftoppm, pdfinfo
    pkgs.tesseract
  ];

  shellHook = ''
    export PATH="${pkgs.poppler_utils}/bin:$PATH"
    echo "Poppler tools available:"
    which pdftoppm
    which pdfinfo
  '';
}