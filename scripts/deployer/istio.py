class IstioDeployer():
    def __init__(self, shell, config_file, cluster):
        self.shell = shell
        self.config_file = config_file
        self.cluster = cluster

    def deploy(self, dryrun=False, revision=None):
        command = ["istioctl", "install", "-f", self.config_file, "--force", "--skip-confirmation", "--context", self.cluster]

        if dryrun:
            command.extend(["--dry-run"])

        if revision != None:
            command.extend(["--revision", revision])

        output = self.shell.execute(command)
        print(output)
        
    def diff(self, revision=None):
        generate_manifest_command = ["istioctl", "manifest", "generate", "-f", self.config_file]

        if revision != None:
            generate_manifest_command.extend(["--revision", revision])

        output = self.shell.execute(generate_manifest_command)

        text_file = open(self.config_file+".output.yaml", "w")
        n = text_file.write(output)
        text_file.close()

        create_dir_command = ["mkdir", self.config_file+".dir"]
        self.shell.execute(create_dir_command)

        split_manifest_command = ["kubectl-slice", "-f", self.config_file+".output.yaml", "-o", self.config_file+".dir", "--exclude-kind", "CustomResourceDefinition"]
        self.shell.execute(split_manifest_command)

        diff_command = ["kubectl", "diff", "-f", self.config_file+".dir", "--context", self.cluster]
        output = self.shell.execute(diff_command)
        print(output)

