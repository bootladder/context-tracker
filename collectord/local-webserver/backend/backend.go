package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os/exec"

	"github.com/julienschmidt/httprouter"
	"github.com/pkg/errors"
)

var debug = false

type ShellHistoryRequest struct {
	SearchQuery string
}

func main() {

	router := httprouter.New()

	// Serve the Frontend
	router.ServeFiles("/*filepath", http.Dir("../frontend"))

	// Serve the API
	router.POST("/api/", gitStatusHandler)
	router.POST("/api/contextlist", contextListHandler)
	router.POST("/api/shellhistory", shellHistoryHandler)
	router.POST("/api/firefoxhistory", firefoxHistoryHandler)

	fmt.Println("Serving on 9999")
	http.ListenAndServe(":9999", router)
}

func jsonHttpResponse(w http.ResponseWriter, body string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte((body)))
}

func firefoxHistoryHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
	stdout := shellout("/opt/projects/context-tracker/firefox-collector/firefox-collector.py")
	jsonHttpResponse(w, stdout)
}

func shellHistoryHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params) {

	var shellHistoryRequest ShellHistoryRequest
	err := json.NewDecoder(r.Body).Decode(&shellHistoryRequest)
	if err != nil {
		fmt.Println("wtf error")
	}

	fmt.Printf("The search query is %s\n", shellHistoryRequest.SearchQuery)

	command := "/opt/projects/context-tracker/ash-collector/ash_collector_oneshot.py"

	var stdout string
	if shellHistoryRequest.SearchQuery != "" {
		stdout = shellout_onearg(command, shellHistoryRequest.SearchQuery)
	} else {
		stdout = shellout(command)
	}

	fmt.Printf("The command is %s\n", command)
	fmt.Printf("The stdout is %s\n", stdout)

	jsonHttpResponse(w, stdout)
}

func contextListHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
	stdout := shellout("./context-list.sh")
	jsonHttpResponse(w, stdout)
}

func gitStatusHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
	stdout := shellout("./context-gitstatus.sh")
	jsonHttpResponse(w, stdout)
}

func shellout(str string) string {
	cmd := exec.Command(str)
	stdout, err := cmd.Output()

	if err != nil {
		fmt.Println(err.Error())
		return "fail to shellout"
	}

	return string(stdout)
}

func shellout_onearg(str string, arg string) string {
	cmd := exec.Command(str, arg)
	stdout, err := cmd.Output()

	if err != nil {
		fmt.Println(err.Error())
		return "fail to shellout: " + err.Error()
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
