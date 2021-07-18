module ShellHistory exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)

import Http

import String
import Json.Decode exposing (..)
import Time exposing (..)
import Date

-- MAIN


main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }



-- MODEL


type alias Model =
    { debugBreadcrumb : String
    , gitStatus : String
    , rows : List (ShellHistoryRow)
    }


-- INIT

dummyPosixTime = Time.millisToPosix 0

init : () -> ( Model, Cmd Msg )
init _ =
    -- The initial model comes from a Request, now it is hard coded
    ( Model
          "dummy debug"
          "dummy status"
          []
    , Cmd.batch [(httpRequestShellHistory)]
    )



-- UPDATE


type Msg
    = Hello Int
    | ReceivedShellHistory (Result Http.Error (List (ShellHistoryRow)))


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Hello a ->
            ( model

            , Cmd.none
            )

        ReceivedShellHistory result ->
            case result of
                Ok status ->
                    ( {model | rows = status}, Cmd.none )

                Err e -> 
                    ( {model | rows = [ShellHistoryRow dummyPosixTime "blah" "blah"]}, Cmd.none)

-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW


posixToHourMinSec : Time.Zone -> Time.Posix -> String
posixToHourMinSec zone posix =
       (String.padLeft 2 '0' <| String.fromInt <| Time.toHour zone posix)
    ++ ":"
    ++ (String.padLeft 2 '0' <| String.fromInt <| Time.toMinute zone posix)
    ++ ":"
    ++ (String.padLeft 2 '0' <| String.fromInt <| Time.toSecond zone posix)


timestampString : Time.Posix -> String
timestampString time = (Date.format "y-MM-d " <| (Date.fromPosix utc time))
                ++ (posixToHourMinSec utc time)

renderShellHistoryRow : ShellHistoryRow -> Html Msg
renderShellHistoryRow row =
    tr []
        [
        td [id "hello"] [text <| timestampString row.starttime]
        , td [id "hello"] [text row.cwd]
        , td [id "hello"] [text row.command]
        ]
      
  
renderShellHistoryTable : List (ShellHistoryRow) -> Html Msg
renderShellHistoryTable rows = 
    table [class "table"]
      [
        tbody [] 
          (List.map renderShellHistoryRow rows)
      ]
    

view : Model -> Html Msg
view model =
    div [id "container"] 
    (List.append
      [ h2 [] [text "Shell History"]
      ]
      
      [(renderShellHistoryTable model.rows)
      ]
    )



-- HTTP

httpRequestShellHistory : Cmd Msg
httpRequestShellHistory =
    Http.post
        { body =
            (Http.stringBody "hello" "wtf")
        , url = "http://localhost:9999/api/shellhistory"
        , expect = Http.expectJson ReceivedShellHistory shellHistoryDecoder
        }


type alias ShellHistoryRow = 
  { starttime : Time.Posix
  , command : String
  , cwd : String
  }

decodePosixTime : Decoder Time.Posix
decodePosixTime =
    int
        |> andThen
            (\ms ->
                succeed <| Time.millisToPosix (ms * 1000)
            )

shellHistoryDecoder : Decoder (List ShellHistoryRow)
shellHistoryDecoder =
    Json.Decode.list (shellHistoryRowDecoder)

shellHistoryRowDecoder : Decoder ShellHistoryRow
shellHistoryRowDecoder =
    map3 ShellHistoryRow
        (field "starttime" decodePosixTime)
        (field "command" string)
        (field "cwd" string)
