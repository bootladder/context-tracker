module ShellHistory exposing (..)

import Browser
import Date
import Debug exposing (toString)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http exposing (..)
import Json.Decode exposing (..)
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
    , gitStatus : String
    , rows : List ShellHistoryRow
    , searchquerystring : String
    , searchsizeint : Int
    , localtimezone : Zone
    , searchquerytypeandchecked : Bool
    , searchquerytypeorchecked : Bool
    }



-- INIT


dummyPosixTime =
    Time.millisToPosix 0


init : () -> ( Model, Cmd Msg )
init _ =
    -- The initial model comes from a Request, now it is hard coded
    ( Model
        "dummy debug"
        "dummy status"
        []
        ""
        -- querystring
        10
        -- search size
        utc
        False
        False
      --zone
    , Cmd.batch [ httpRequestShellHistory, getLocalTimeZone ]
    )



-- UPDATE


type Msg
    = Hello Int
    | ReceivedShellHistory (Result Http.Error (List ShellHistoryRow))
    | SearchButtonClicked
    | SearchInputHappened String
    | SearchSizeInputHappened String
    | SearchQueryTypeANDCheckedHappened Bool
    | SearchQueryTypeORCheckedHappened Bool
    | GotTimeZone Zone


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
                    ( { model | rows = status }, Cmd.none )

                Err e ->
                    ( { model | rows = [ ShellHistoryRow dummyPosixTime "failtoparse" (errorToString e) ] }, Cmd.none )

        SearchButtonClicked ->
            ( model, Cmd.batch [ httpRequestShellHistoryWithSearch model.searchquerystring ] )

        SearchInputHappened str ->
            ( { model | searchquerystring = str }, Cmd.none )

        SearchSizeInputHappened str ->
            ( { model
                | searchsizeint =
                    case String.toInt str of
                        Just i ->
                            i

                        Nothing ->
                            10
              }
            , Cmd.none
            )

        SearchQueryTypeANDCheckedHappened b ->
            ( {model | searchquerytypeorchecked = b}
            ,Cmd.none)

        SearchQueryTypeORCheckedHappened b ->
            ( {model | searchquerytypeorchecked = b}
            ,Cmd.none)

        GotTimeZone z ->
            ( { model | localtimezone = z }, Cmd.none )

-- http
errorToString : Http.Error -> String
errorToString error =
    case error of
        BadUrl url ->
            "The URL " ++ url ++ " was invalid"
        Timeout ->
            "Unable to reach the server, try again"
        NetworkError ->
            "Unable to reach the server, check your network connection"
        BadStatus 500 ->
            "The server had a problem, try again later"
        BadStatus 400 ->
            "Verify your information and try again"
        BadStatus _ ->
            "Unknown error"
        BadBody errorMessage ->
            errorMessage

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


timestampString : Time.Posix -> Time.Zone -> String
timestampString time zone =
    (Date.format "y-MM-d " <| Date.fromPosix zone time)
        ++ posixToHourMinSec zone time


renderShellHistoryRow : ShellHistoryRow -> Time.Zone -> Html Msg
renderShellHistoryRow row zone =
    tr []
        [ td [ id "hello" ] [ text <| timestampString row.timestamp zone ]
        , td [ id "hello" ] [ text row.pwd ]
        , td [ id "hello" ] [ text row.command ]
        ]


renderShellHistoryTable : List ShellHistoryRow -> Time.Zone -> Html Msg
renderShellHistoryTable rows zone =
    table [ class "table" ]
        [ tbody []
            (List.map (\row -> renderShellHistoryRow row zone) rows )
        ]

renderPwdSearch: Model -> Html Msg
renderPwdSearch model =
    div []
                [
                 span [] [text "pwd"]
                , input [ onInput SearchInputHappened ] []
                , button [ onClick SearchButtonClicked ] [ text "search" ]

                ]

renderCommandSearch: Model -> Html Msg
renderCommandSearch model =
    div []
                [
                  span [] [text "command"]
                , input [ onInput SearchInputHappened ] []
                , button [ onClick SearchButtonClicked ] [ text "search" ]
                ]

renderQueryTypeSelector : Model -> Html Msg
renderQueryTypeSelector model =
    div []
    [
        div []
        [
            span [] [text "AND"]
            ,input [ type_ "checkbox", onCheck SearchQueryTypeANDCheckedHappened] []

         ]
         , div []
         [
         span [] [text "OR"]
         ,input [ type_ "checkbox", onCheck SearchQueryTypeORCheckedHappened] []
         ]

    ]


renderPaginator: Model -> Html Msg
renderPaginator model =
    div [class "form-group row"]
        [
            div [class "col-xs-2"] [
            input [
            onInput SearchSizeInputHappened,
            Html.Attributes.value <| toString model.searchsizeint
            ] []
            ]
         ,
         div [class "col-xs-4"] [

                     button [] [ text "<" ]
                     , span [] [ text "10/20" ]
                     , button [] [ text ">" ]
                     , span [] [ text "spacer" ]
                     ]
         ]


renderHeader : Model -> Html Msg
renderHeader model =
    div []
        [ h2 [] [ text "Shell History" ]
        , renderPwdSearch model
        , renderCommandSearch model
        , renderQueryTypeSelector model
        , renderPaginator model
        ]


view : Model -> Html Msg
view model =
    div
        [ id "shell-history-container"
        , class "bg-light"
        ]
        (List.append
            [ renderHeader model
            ]
            [ renderShellHistoryTable model.rows model.localtimezone
            ]
        )



-- HTTP


httpRequestShellHistory : Cmd Msg
httpRequestShellHistory =
    let
        jsonBody =
            "{ \"searchquery\" : \"" ++ "\"}"
    in
    Http.post
        { body =
            Http.stringBody "application/json" jsonBody
        , url = "http://localhost:9999/api/shellhistory"
        , expect = Http.expectJson ReceivedShellHistory shellHistoryDecoder
        }


httpRequestShellHistoryWithSearch : String -> Cmd Msg
httpRequestShellHistoryWithSearch querystr =
    let
        jsonBody =
            "{ \"searchquery\" : \""
                ++ querystr
                ++ "\"}"
    in
    Http.post
        { body =
            Http.stringBody "application/json" jsonBody
        , url = "http://localhost:9999/api/shellhistory"
        , expect = Http.expectJson ReceivedShellHistory shellHistoryDecoder
        }


type alias ShellHistoryRow =
    { timestamp : Time.Posix
    , command : String
    , pwd : String
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
    Json.Decode.list shellHistoryRowDecoder


shellHistoryRowDecoder : Decoder ShellHistoryRow
shellHistoryRowDecoder =
    map3 ShellHistoryRow
        (field "timestamp" decodePosixTime)
        (field "command" string)
        (field "pwd" string)


getLocalTimeZone : Cmd Msg
getLocalTimeZone =
    Task.perform GotTimeZone Time.here
