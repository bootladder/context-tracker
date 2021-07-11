module ShellHistory exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)

import Http

import String
import Json.Decode exposing (..)
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
    , rows : List (ShellHistoryRow)
    }


-- INIT


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
                    ( {model | rows = [ShellHistoryRow 1 "blah" "blah"]}, Cmd.none)

-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW

renderShellHistoryRow : ShellHistoryRow -> Html Msg
renderShellHistoryRow row =
  div [] [
            div [id "hello"] [text "fucking elm parsing time"]
          , div [id "hello"] [text row.cwd]
          , div [id "hello"] [text row.command]
          ]
  
    

view : Model -> Html Msg
view model =
    div [id "container"] 
    (List.append
      [ h2 [] [text "Hurr durr title"]
      , div [] [text model.gitStatus]
      ]

      (List.map renderShellHistoryRow model.rows)
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
  { starttime : Int
  , command : String
  , cwd : String
  }

shellHistoryDecoder : Decoder (List ShellHistoryRow)
shellHistoryDecoder =
    Json.Decode.list (shellHistoryRowDecoder)

shellHistoryRowDecoder : Decoder ShellHistoryRow
shellHistoryRowDecoder =
    map3 ShellHistoryRow
        (field "starttime" int)
        (field "command" string)
        (field "cwd" string)
