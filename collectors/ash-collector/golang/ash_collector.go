package main

import (
  "database/sql"
  _ "github.com/mattn/go-sqlite3" // Import go-sqlite3 library
  "fmt"
)


func main() {

  fmt.Print("hello")
  sqliteDatabase, err := sql.Open("sqlite3", "/home/steve/.ash/history.db") // Open the created SQLite File
  defer sqliteDatabase.Close() // Defer Closing the database

  if err != nil {
    fmt.Print("FAIL OPENING")
  }


  fmt.Print("hello2")

  row, err := sqliteDatabase.Query("SELECT * FROM commands limit 10")
  if err != nil {
    fmt.Print("FAIL 3")
    return
  }
  defer row.Close()


  for row.Next() { // Iterate and fetch the records from result cursor
    fmt.Print("hello")
    var id int
    var code string
    var name string
    var program string
    row.Scan(&id, &code, &name, &program)

    fmt.Print("id: ", id)
  }
}
