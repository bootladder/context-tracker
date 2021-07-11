package main

import (
	"fmt"
	"github.com/fsnotify/fsnotify"
	"path/filepath"
	"os"
	"time"
)

// filwpath walk will not follow symlinks
//directoryToWatch := "/opt/contexts/test/link_to_context"
var directoryToWatch = "/home/steve/scrap/testcontextdata/"
var outputFilePath = "/opt/contexts/test/track-filesystem.txt"


var watcher *fsnotify.Watcher

func main() {

	printHello()

	watcher = create_new_fsnotify_watcher()
	defer watcher.Close()

	watchDirectoryRecursive(directoryToWatch)

	done := make(chan bool)

	go func() {
		for {
			select {
				case event := <-watcher.Events:
     				handleFsNotifyEvent(&event)

				case err := <-watcher.Errors:
					fmt.Println("ERROR", err)
			}
		}
	}()

	<-done
}

func printHello() {
	fmt.Println("Context Tracker: Filesystem")
	fmt.Println("Version 0.0 blah")
	fmt.Println("Watches directory recursively and outputs events to file")
	fmt.Println("If 2 arguments supplied, they are the watch directory and output file")
	fmt.Println("Else, watches the current directory and outputs to the current directory")
	fmt.Println()
}

func watchDirectoryRecursive(dir string) {
	if err := filepath.Walk(dir, watchDir); err != nil {
		fmt.Println("ERROR: Walk watchDir", err)
		panic("ERROR WALKING")
	}
}

func watchDir(path string, fi os.FileInfo, err error) error {
	if fi.Mode().IsDir() {
		fmt.Println("Adding path " + path + " to watcher")
		return watcher.Add(path)
	}
	return nil
}

func create_new_fsnotify_watcher() *fsnotify.Watcher{

	w, err := fsnotify.NewWatcher()
	if err != nil {
		fmt.Println("ERROR COULD NOT CREATE WATCHER", err)
		panic("COULD NOT CREATE WATCHER")
	}

	return w
}


func handleFsNotifyEvent(event * fsnotify.Event) {
	fmt.Printf("EVENT! %#v\n", event)
	fmt.Printf("EVENTSTRING! %s\n", event.String())

	readabletimestamp := time.Now().Format("2006-01-02 15:04:05")
	outputString := fmt.Sprintf("%d", (time.Now().Unix())) + "," + readabletimestamp + "," + event.Name + "," + event.Op.String() + "\n"

	writeToOutputFile(outputString)

}

func writeToOutputFile(str string) {
	f, err := os.OpenFile(outputFilePath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		fmt.Println(err)
		panic("COULD NOT OPEN TO OUTPUT FILE")
	}

	defer f.Close()
	if _, err := f.WriteString(str); err != nil {
		fmt.Println(err)
	}
}
