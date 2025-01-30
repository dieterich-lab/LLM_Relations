# To be replaced with the same function on line 284  in file langchain_core/messages/utils.py of the library langchain_core==0.3.31


def _convert_to_message(message: MessageLikeRepresentation) -> BaseMessage:
    """Instantiate a message from a variety of message formats.

    The message format can be one of the following:

    - BaseMessagePromptTemplate
    - BaseMessage
    - 2-tuple of (role string, template); e.g., ("human", "{user_input}")
    - dict: a message dict with role and content keys
    - string: shorthand for ("human", template); e.g., "{user_input}"

    Args:
        message: a representation of a message in one of the supported formats.

    Returns:
        an instance of a message or a message template.

    Raises:
        NotImplementedError: if the message type is not supported.
        ValueError: if the message dict does not contain the required keys.
    """
    if isinstance(message, BaseMessage):
        _message = message
        if hasattr(_message, "invalid_tool_calls") and hasattr(
            _message, "invalid_tool_calls"
        ):
            _message.invalid_tool_calls = list()
            if (
                "message" in _message.response_metadata
                and "tool_calls" in _message.response_metadata["message"]
            ):
                if (
                    "triples"
                    in _message.response_metadata["message"]["tool_calls"][0][
                        "function"
                    ]["arguments"]
                ):
                    obj = repair_json(
                        _message.response_metadata["message"]["tool_calls"][0][
                            "function"
                        ]["arguments"]["triples"]
                    )
                    _message.response_metadata["message"]["tool_calls"][0]["function"][
                        "arguments"
                    ]["triples"] = obj
                elif (
                    "proteins"
                    in _message.response_metadata["message"]["tool_calls"][0][
                        "function"
                    ]["arguments"]
                ):
                    if not isinstance(
                        _message.response_metadata["message"]["tool_calls"][0][
                            "function"
                        ]["arguments"],
                        str,
                    ):
                        try:
                            obj = str(
                                _message.response_metadata["message"]["tool_calls"][0][
                                    "function"
                                ]["arguments"]["proteins"]
                            )
                        except:
                            obj = repair_json(
                                _message.response_metadata["message"]["tool_calls"][0][
                                    "function"
                                ]["arguments"]["proteins"]
                            )
                        _message.response_metadata["message"]["tool_calls"][0][
                            "function"
                        ]["arguments"]["proteins"] = obj
                    else:
                        obj = _message.response_metadata["message"]["tool_calls"][0][
                            "function"
                        ]["arguments"]
                elif (
                    "genes_and_transcriptionfactors"
                    in _message.response_metadata["message"]["tool_calls"][0][
                        "function"
                    ]["arguments"]
                ):
                    if not isinstance(
                        _message.response_metadata["message"]["tool_calls"][0][
                            "function"
                        ]["arguments"],
                        str,
                    ):
                        try:
                            obj = str(
                                _message.response_metadata["message"]["tool_calls"][0][
                                    "function"
                                ]["arguments"]["genes_and_transcriptionfactors"]
                            )
                        except:
                            obj = repair_json(
                                _message.response_metadata["message"]["tool_calls"][0][
                                    "function"
                                ]["arguments"]["genes_and_transcriptionfactors"]
                            )
                        _message.response_metadata["message"]["tool_calls"][0][
                            "function"
                        ]["arguments"]["genes_and_transcriptionfactors"] = obj
                    else:
                        obj = _message.response_metadata["message"]["tool_calls"][0][
                            "function"
                        ]["arguments"]
                else:
                    obj = str(
                        _message.response_metadata["message"]["tool_calls"][0][
                            "function"
                        ]["arguments"]
                    )
            elif "tool_calls" in _message.additional_kwargs:
                obj = repair_json(
                    _message.additional_kwargs["tool_calls"][0]["function"]["arguments"]
                )
                _message.additional_kwargs["tool_calls"][0]["function"][
                    "arguments"
                ] = obj
            else:
                obj = str(list())
            _message.content = obj  # NEW
    elif (
        isinstance(message, dict)
        and "raw" in message
        and isinstance(message["raw"], BaseMessage)
    ):
        _message = message["raw"]
        if (
            hasattr(_message, "response_metadata")
            and "message" in _message.response_metadata
            and "tool_calls" in _message.response_metadata["message"]
        ):
            if (
                "triples"
                in _message.response_metadata["message"]["tool_calls"][0]["function"][
                    "arguments"
                ]
            ):
                obj = repair_json(
                    str(
                        _message.response_metadata["message"]["tool_calls"][0][
                            "function"
                        ]["arguments"]["triples"]
                    )
                )
                _message.response_metadata["message"]["tool_calls"][0]["function"][
                    "arguments"
                ] = obj
            elif (
                "proteins"
                in _message.response_metadata["message"]["tool_calls"][0]["function"][
                    "arguments"
                ]
            ):
                obj = repair_json(
                    str(
                        _message.response_metadata["message"]["tool_calls"][0][
                            "function"
                        ]["arguments"]["proteins"]
                    )
                )
                _message.response_metadata["message"]["tool_calls"][0]["function"][
                    "proteins"
                ] = obj
            elif (
                "genes_and_transcriptionfactors"
                in _message.response_metadata["message"]["tool_calls"][0]["function"][
                    "arguments"
                ]
            ):
                obj = repair_json(
                    str(
                        _message.response_metadata["message"]["tool_calls"][0][
                            "function"
                        ]["arguments"]["genes_and_transcriptionfactors"]
                    )
                )
                _message.response_metadata["message"]["tool_calls"][0]["function"][
                    "genes_and_transcriptionfactors"
                ] = obj
            else:
                obj = str(list())
                _message.response_metadata["message"]["tool_calls"][0]["function"][
                    "arguments"
                ] = obj
        elif "tool_calls" in _message.additional_kwargs:
            obj = repair_json(
                _message.additional_kwargs["tool_calls"][0]["function"]["arguments"]
            )
            _message.additional_kwargs["tool_calls"][0]["function"]["arguments"] = obj
        else:
            obj = str(list())
        _message.content = obj  # NEW
    elif isinstance(message, str):
        _message = _create_message_from_message_type("human", message)
    elif isinstance(message, Sequence) and len(message) == 2:
        # mypy doesn't realise this can't be a string given the previous branch
        message_type_str, template = message  # type: ignore[misc]
        _message = _create_message_from_message_type(message_type_str, template)
    elif isinstance(message, dict):
        msg_kwargs = message.copy()
        try:
            try:
                msg_type = msg_kwargs.pop("role")
            except KeyError:
                msg_type = msg_kwargs.pop("type")
            # None msg content is not allowed
            msg_content = msg_kwargs.pop("content") or ""
        except KeyError as e:
            msg = f"Message dict must contain 'role' and 'content' keys, got {message}"
            msg = create_message(
                message=msg, error_code=ErrorCode.MESSAGE_COERCION_FAILURE
            )
            raise ValueError(msg) from e
        _message = _create_message_from_message_type(
            msg_type, msg_content, **msg_kwargs
        )
    else:
        msg = f"Unsupported message type: {type(message)}"
        msg = create_message(message=msg, error_code=ErrorCode.MESSAGE_COERCION_FAILURE)
        raise NotImplementedError(msg)

    return _message
