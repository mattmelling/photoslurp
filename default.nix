{ pkgs ? import <nixpkgs> {} }:
with pkgs;
pkgs.python37Packages.buildPythonApplication rec {
  name = "photoslurp";
  src = ./.;
  propagatedBuildInputs = [
    (pkgs.python37.withPackages(ps: with ps; [
      exifread
      av
      plac
    ]))
  ];
}
