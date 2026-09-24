{
  # Dev shell for this specification set: the Python the document gates need.
  # No Lean yet -- tau-web's TauWeb.Relay carries the formal companion (F4).
  description = "paid-tcp-relay specification gates";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/aff8a0b28396750446e5537a96461bc4facdb287";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAll = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in {
      devShells = forAll (pkgs: {
        default = pkgs.mkShell {
          packages = [ pkgs.python3 pkgs.git ];
        };
      });

      # `nix flake check` runs the same gates CI does.
      checks = forAll (pkgs: {
        gates = pkgs.runCommand "paid-tcp-relay-gates"
          { nativeBuildInputs = [ pkgs.python3 pkgs.bash ]; } ''
          cp -r ${self} src && chmod -R u+w src && cd src
          bash tools/check-all.sh
          touch $out
        '';
      });
    };
}
