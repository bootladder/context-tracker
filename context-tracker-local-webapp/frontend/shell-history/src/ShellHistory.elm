module ShellHistory exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)

import Http

import String
import Json.Decode exposing (..)


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
    , rows : List (List (String))
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
    | ReceivedShellHistory (Result Http.Error (List (List (String))))


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
                Err e -> (model, Cmd.none)

-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW

renderShellHistoryRow : List (String) -> Html Msg
renderShellHistoryRow mystr =
    div [id "hello"] [text "myshellrow"]
  
    

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


shellHistoryDecoder : Decoder (List (List (String)))
shellHistoryDecoder =
    Json.Decode.list (Json.Decode.list string)
