module Main exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)

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
    }


-- INIT


init : () -> ( Model, Cmd Msg )
init _ =
    -- The initial model comes from a Request, now it is hard coded
    ( Model
        "dummy debug"
    , Cmd.none
    )



-- UPDATE


type Msg
    = Hello Int


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Hello a ->
            ( model

            , Cmd.none
            )

-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW


view : Model -> Html Msg
view model =
    div [id "container"] 
    [ h2 [] [text "hello"]
    ]
