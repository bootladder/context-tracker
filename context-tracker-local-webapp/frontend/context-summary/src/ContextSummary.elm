module ContextSummary exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)

import Http

import String


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
    , contextNames : List(String)
    }


-- INIT


init : () -> ( Model, Cmd Msg )
init _ =
    -- The initial model comes from a Request, now it is hard coded
    ( Model
          "dummy debug"
          ["context 1"]
    , Cmd.batch [(httpRequestContextList)]
    )



-- UPDATE


type Msg
    = Hello Int
    | ReceivedContextList (Result Http.Error (String))


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Hello a ->
            ( model

            , Cmd.none
            )

        ReceivedContextList result ->
            case result of
                Ok names ->
                    ( {model | contextNames = String.split " " names}, Cmd.none )
                Err e -> (model, Cmd.none)

-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW


view : Model -> Html Msg
view model =
    div [id "container"] 
    [ h2 [] [text "Context Summary"]
    , div [] [text (String.join " " model.contextNames)]
    ]



-- HTTP

httpRequestContextList : Cmd Msg
httpRequestContextList =
    Http.post
        { body =
            (Http.stringBody "hello" "wtf")
        , url = "http://localhost:9999/api/contextlist"
        , expect = Http.expectString ReceivedContextList
        }
