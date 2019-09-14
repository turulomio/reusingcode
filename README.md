# reusingcode
Code that I reuse in several projects

# Function for python setups

    def download_from_github(self,user,repository,path_filename, destiny_directory):
        cwd=os.getcwd()
        os.system("touch '{}/{}'".format(destiny_directory,os.path.basename(path_filename)))
        os.system("rm '{}/{}'".format(destiny_directory, os.path.basename(path_filename)))
        os.chdir(destiny_directory)
        comand="wget -q https://raw.githubusercontent.com/{}/{}/master/{}  --no-clobber".format(user,repository, path_filename)
        print (comand)
        os.system(comand)
        #os.system("sed -i -e '3i ## THIS FILE HAS BEEN DOWNLOADED AT {} FROM https://github.com/{}/{}/{}.' {}".format(datetime.now(),user,repository,path_filename,os.path.basename(path_filename)))
        print("Updated {}".format(path_filename))
        os.chdir(cwd)


## Example
        self.download_from_github('turulomio','reusingcode','python/connection_pg.py', 'caloriestracker')
