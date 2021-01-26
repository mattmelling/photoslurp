{
  description = "photoslurp media renamer";
  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
        overlays = [ self.overlay ];
      };
    in {
      overlay = final: prev: {
        photoslurp = prev.callPackage ./default.nix { };
      };
    };
}
