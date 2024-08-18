{
  description = "ctf dev environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };

      python = pkgs.python311.withPackages (p: with p; [ 
        angr
        ipython 
        ipdb
        python-lsp-server
      ]);
    in
    {
      devShells.default = pkgs.mkShell {
        buildInputs = [ 
          python 
          pkgs.radare2 
        ];

        shellHook = ''
          echo "Welcome to the pwn.college dev shell!"
          export PYTHONPATH=$PWD
        '';
      };
    });
}

