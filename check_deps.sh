#!/bin/bash

# Ensure the RPM package path is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 path_to_rpm_package"
    exit 1
fi

rpm_package=$1

# Get a list of dependencies for the RPM package
dependencies=$(rpm -qpR $rpm_package)

# An array to hold the package names
packages=()

for dep in $dependencies; do
    # Find which package provides the capability or shared library
    provider=$(yum -q provides "$dep" | grep -E '^([a-zA-Z0-9\-]+\.?)+\.' | head -n 1 | awk '{print $1}')
    
    # If the package is not installed, add it to the list
    if ! rpm -q $provider >/dev/null 2>&1; then
        packages+=("$provider")
    fi
done

# Extract just the package name, stripping off the version numbers and arch
clean_packages=()
for pkg in "${packages[@]}"; do
    pkg_name=$(echo "$pkg" | sed -E 's/-[0-9]+(\.[0-9]+)*-.*$//')
    clean_packages+=("$pkg_name")
done

# Print the unique not-installed package names separated by spaces
echo ${clean_packages[@]} | tr ' ' '\n' | sort -u | tr '\n' ' '
