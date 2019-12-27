{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = [
    (pkgs.python37.withPackages(ps: with ps; [
      exifread
      av
      plac
    ]))
  ];
}
