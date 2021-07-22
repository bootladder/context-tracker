module FirefoxHistory exposing (..)

import Browser
import Date exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Json.Decode exposing (..)
import String exposing (..)
import Time exposing (..)



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
    , rows : List FirefoxHistoryRow
    }



-- INIT


dummyPosixTime =
    Time.millisToPosix 0


init : () -> ( Model, Cmd Msg )
init _ =
    -- The initial model comes from a Request, now it is hard coded
    ( Model
        "dummy debug"
        []
    , Cmd.batch [ httpRequestFirefoxHistory ]
    )



-- UPDATE


type Msg
    = Hello Int
    | ReceivedFirefoxHistory (Result Http.Error (List FirefoxHistoryRow))


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Hello a ->
            ( model
            , Cmd.none
            )

        ReceivedFirefoxHistory result ->
            case result of
                Ok status ->
                    ( { model | rows = status }, Cmd.none )

                Err e ->
                    let
                        _ =
                            Debug.log "error is " e
                    in
                    ( { model | rows = [ FirefoxHistoryRow dummyPosixTime "blahurl" (Just "blahtitle") (Just "blahdesc") ] }, Cmd.none )



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
timestampString time =
    (Date.format "y-MM-d " <| Date.fromPosix utc time)
        ++ posixToHourMinSec utc time


renderFirefoxHistoryRow : FirefoxHistoryRow -> Html Msg
renderFirefoxHistoryRow row =
    tr []
        [ td [ id "hello" ] [ text <| timestampString row.last_visit_date ]
        , td [ id "hello" ] [ text row.url ]
        , td [ id "hello" ]
            [ case row.title of
                Just a ->
                    text a

                Nothing ->
                    text "nothing"
            ]
        ]


renderFirefoxHistoryTable : List FirefoxHistoryRow -> Html Msg
renderFirefoxHistoryTable rows =
    table [ class "table" ]
        [ tbody []
            (List.map renderFirefoxHistoryRow rows)
        ]


view : Model -> Html Msg
view model =
    div [ id "container" ]
        (List.append
            [ h2 [] [ text "Firefox History" ]
            ]
            [ renderFirefoxHistoryTable model.rows
            ]
        )



-- HTTP


httpRequestFirefoxHistory : Cmd Msg
httpRequestFirefoxHistory =
    Http.post
        { body =
            Http.stringBody "hello" "wtf"
        , url = "http://localhost:9999/api/firefoxhistory"
        , expect = Http.expectJson ReceivedFirefoxHistory firefoxHistoryDecoder
        }


type alias FirefoxHistoryRow =
    { last_visit_date : Time.Posix
    , url : String
    , title : Maybe String
    , description : Maybe String
    }



-- PAY ATTENTION TO MICROS OR MILLIS OR SECS


decodePosixTime : Decoder Time.Posix
decodePosixTime =
    int
        |> andThen
            (\ms ->
                succeed <| Time.millisToPosix <| round (Basics.toFloat ms / 1000.0)
            )


firefoxHistoryDecoder : Decoder (List FirefoxHistoryRow)
firefoxHistoryDecoder =
    Json.Decode.list firefoxHistoryRowDecoder


firefoxHistoryRowDecoder : Decoder FirefoxHistoryRow
firefoxHistoryRowDecoder =
    map4 FirefoxHistoryRow
        (field "last_visit_date" decodePosixTime)
        (field "url" string)
        (maybe <| field "title" string)
        (maybe <| field "description" string)
