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

	router.ServeFiles("/*filepath", http.Dir("../frontend"))
	router.POST("/api/", gitStatusHandler)

	fmt.Println("Serving on 9090")
	http.ListenAndServe(":9090", router)
}

// Handler
func gitStatusHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params) {

	// go to the file storage of this context
	// run git status
	cmd := exec.Command("./context-gitstatus.sh", "test")
	stdout, err := cmd.Output()

    if err != nil {
        fmt.Println(err.Error())
        return
    }

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte((string(stdout))))
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
