package main

import (
	"fmt"
	"net/http"
	"os/exec"

	"github.com/julienschmidt/httprouter"
	"github.com/pkg/errors"
)

var debug = false


func main() {

	router := httprouter.New()

  // Serve the Frontend
	router.ServeFiles("/*filepath", http.Dir("../frontend"))

  // Serve the API
	router.POST("/api/", gitStatusHandler)
	router.POST("/api/contextlist", contextListHandler)
	router.POST("/api/shellhistory", shellHistoryHandler)

	fmt.Println("Serving on 9999")
	http.ListenAndServe(":9999", router)
}


func shellHistoryHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
	stdout := shellout("/opt/projects/context-tracker/ash-collector/ash_collector.py")

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte((stdout)))
}

func contextListHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
	stdout := shellout("./context-list.sh")

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte((stdout)))
}

func gitStatusHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params) {

	stdout := shellout("./context-gitstatus.sh")

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte((stdout)))
}

func shellout(str string) string {
	cmd := exec.Command(str, "test")
	stdout, err := cmd.Output()

    if err != nil {
        fmt.Println(err.Error())
        return "fail to shellout"
    }

	return string(stdout)
}


func fatal(err error, msgs ...string) {
	if err != nil {
		var str string
		for _, msg := range msgs {
			str = msg
			break
		}
		panic(errors.Wrap(err, str))
	}
}

func printf(s string, a ...interface{}) {
	fmt.Printf(s, a...)
}
