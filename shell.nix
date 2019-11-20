with import <nixpkgs> {};
stdenv.mkDerivation {
  name = "photoslurp";
  buildInputs = [
    (python37.withPackages(ps: with ps; [
      exifread
      av
      plac
    ]))
  ];
}
