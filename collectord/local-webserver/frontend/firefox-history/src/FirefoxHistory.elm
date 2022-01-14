module FirefoxHistory exposing (..)

import Browser
import Date exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Json.Decode exposing (..)
import Maybe exposing (withDefault)
import String exposing (..)
import Task exposing (perform)
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
    , localtimezone : Time.Zone
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
        utc
    , Cmd.batch [ httpRequestFirefoxHistory, getLocalTimeZone ]
    )



-- UPDATE


type Msg
    = Hello Int
    | ReceivedFirefoxHistory (Result Http.Error (List FirefoxHistoryRow))
    | GotTimeZone Zone


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

        GotTimeZone z ->
            ( { model | localtimezone = z }, Cmd.none )



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


timestampString : Time.Zone -> Time.Posix -> String
timestampString zone time =
    (Date.format "y-MM-dd " <| Date.fromPosix utc time)
        ++ posixToHourMinSec zone time


renderFirefoxHistoryRow : Time.Zone -> ( FirefoxHistoryRow, Int ) -> Html Msg
renderFirefoxHistoryRow zone ( row, index ) =
    let
        urllength =
            length row.url

        truncateUrlIfLarge str =
            if urllength > 40 then
                slice 0 40 str ++ "..."

            else
                str
    in
    tr
        [ if modBy 2 index == 0 then
            class "alt-row-color"

          else
            class "blah"
        ]
        [ td [ id "hello" ] [ text <| timestampString zone row.timestamp ]
        , td [ id "hello" ]
            [ div []
                [ text <| truncateUrlIfLarge row.url
                ]
            ]
        , td [ id "hello" ]
            [ text <| withDefault "nothing" row.title
            ]
        ]


sortByTimestamp a b =
    let
        atimeint =
            posixToMillis <| a.timestamp

        btimeint =
            posixToMillis <| b.timestamp
    in
    case Basics.compare atimeint btimeint of
        LT ->
            GT

        GT ->
            LT

        EQ ->
            EQ


renderFirefoxHistoryTable : Time.Zone -> List FirefoxHistoryRow -> Html Msg
renderFirefoxHistoryTable zone rows =
    let
        sortedRows =
            rows |> List.sortWith sortByTimestamp
    in
    table [ class "table" ]
        [ tbody []
            (List.indexedMap (\i row -> renderFirefoxHistoryRow zone ( row, i )) sortedRows)
        ]


view : Model -> Html Msg
view model =
    div [ id "container" ]
        (List.append
            [ h2 [] [ text "Firefox History" ]
            ]
            [ renderFirefoxHistoryTable model.localtimezone model.rows
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
    { timestamp : Time.Posix
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
        (field "timestamp" decodePosixTime)
        (field "url" string)
        (maybe <| field "title" string)
        (maybe <| field "description" string)


getLocalTimeZone : Cmd Msg
getLocalTimeZone =
    Task.perform GotTimeZone Time.here
