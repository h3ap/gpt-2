# Notes

You will get a before/after cleaning of the gpt2 output on stdout.
The script has a class in it. Maybe you have to change the paths.
If you run the script directly from commandline it will create a logger. 
When you import the class you have to specify your logger to the gpt2text object while instantiating it.
To log to a file you have to create a logging file in the directory where you invoke the python command :

```
touch ./bot_logs.txt
```

## Testing in docker

If you have not build the container with the the script, you can mount the directory into the container.
This is also beneficial to work on the file with your editor of choice outside of the container.

```
sudo docker run -v <path to local io_gpt-2 dir>:/gpt-2/io_gpt2 -it <name of container> bash
```

## In Docker Container

Run it like this:

```
python3 ./io_gpt2/IO_gpt2.py "Some crazy Strings you want GPT-2 to receive"
```  
