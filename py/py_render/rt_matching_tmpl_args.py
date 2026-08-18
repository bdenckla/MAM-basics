from __future__ import annotations

from hkq_cmn.supported_qere_wrapper import (
    supported_qere_wrapper_from_template_args,
)


def matching_template_arguments_in_mpu_verse_by_row_number(
    payload: dict[str, object],
) -> dict[str, list[dict[str, str]]]:
    """Return matching template argument records keyed by table row number."""
    rows_obj = payload.get("mam_plus_rows_matching_mpu_verse_template_arg")
    if rows_obj is None:
        return {}
    if not isinstance(rows_obj, list):
        raise ValueError(
            "table_data.json mam_plus_rows_matching_mpu_verse_template_arg must be a list"
        )

    out: dict[str, list[dict[str, str]]] = {}
    for row in rows_obj:
        if not isinstance(row, dict):
            raise ValueError(
                "table_data.json mam_plus_rows_matching_mpu_verse_template_arg must contain only objects"
            )

        row_number = row.get("row_number")
        if not isinstance(row_number, int):
            raise ValueError(
                "mam_plus_rows_matching_mpu_verse_template_arg row has invalid row_number"
            )

        targets_obj = row.get("matching_template_args_in_mpu_verse")
        if targets_obj is None:
            out[str(row_number)] = []
            continue
        out[str(row_number)] = _validated_template_arg_records(
            targets_obj,
            field_name="matching_template_args_in_mpu_verse",
        )

    return out


def supported_qere_wrapper_by_row_number(
    payload: dict[str, object],
) -> dict[str, dict[str, str]]:
    rows_obj = payload.get("mam_plus_rows_with_supported_qere_wrapper")
    if rows_obj is not None:
        if not isinstance(rows_obj, list):
            raise ValueError(
                "table_data.json mam_plus_rows_with_supported_qere_wrapper must be a list"
            )

        out: dict[str, dict[str, str]] = {}
        for row in rows_obj:
            if not isinstance(row, dict):
                raise ValueError(
                    "mam_plus_rows_with_supported_qere_wrapper must contain only objects"
                )

            row_number = row.get("row_number")
            if not isinstance(row_number, int):
                raise ValueError(
                    "mam_plus_rows_with_supported_qere_wrapper row has invalid row_number"
                )

            wrapper_raw = row.get("supported_qere_wrapper_in_mpu_verse")
            wrapper = _validated_supported_qere_wrapper(wrapper_raw)
            if wrapper is not None:
                out[str(row_number)] = wrapper
        return out

    rows_obj = payload.get("mam_plus_rows_matching_mpu_verse_template_arg")
    if rows_obj is None:
        return {}
    if not isinstance(rows_obj, list):
        raise ValueError(
            "table_data.json mam_plus_rows_matching_mpu_verse_template_arg must be a list"
        )

    out: dict[str, dict[str, str]] = {}
    for row in rows_obj:
        if not isinstance(row, dict):
            raise ValueError(
                "mam_plus_rows_matching_mpu_verse_template_arg must contain only objects"
            )

        row_number = row.get("row_number")
        if not isinstance(row_number, int):
            raise ValueError(
                "mam_plus_rows_matching_mpu_verse_template_arg row has invalid row_number"
            )

        all_args_raw = row.get("template_args_in_mpu_verse")
        if all_args_raw is None:
            all_args = []
        else:
            all_args = _validated_template_arg_records(
                all_args_raw,
                field_name="template_args_in_mpu_verse",
            )

        wrapper = supported_qere_wrapper_from_template_args(all_args)
        if wrapper is not None:
            out[str(row_number)] = wrapper

    return out


def _validated_supported_qere_wrapper(
    wrapper_obj: object,
) -> dict[str, str] | None:
    if wrapper_obj is None:
        return None
    if not isinstance(wrapper_obj, dict):
        raise ValueError("supported_qere_wrapper_in_mpu_verse must be an object")

    template_name = wrapper_obj.get("template_name")
    ketiv = wrapper_obj.get("ketiv")
    qere = wrapper_obj.get("qere")
    if not isinstance(template_name, str):
        raise ValueError("supported_qere_wrapper_in_mpu_verse missing template_name")
    if not isinstance(ketiv, str):
        raise ValueError("supported_qere_wrapper_in_mpu_verse missing ketiv")
    if not isinstance(qere, str):
        raise ValueError("supported_qere_wrapper_in_mpu_verse missing qere")

    return {
        "template_name": template_name,
        "ketiv": ketiv,
        "qere": qere,
    }


def _validated_template_arg_records(
    targets_obj: object,
    *,
    field_name: str,
) -> list[dict[str, str]]:
    if not isinstance(targets_obj, list):
        raise ValueError(f"{field_name} must be a list when present")

    targets: list[dict[str, str]] = []
    for target in targets_obj:
        if not isinstance(target, dict):
            raise ValueError(f"{field_name} must contain only objects")

        template_name = target.get("template_name")
        argument_key = target.get("argument_key")
        argument_text = target.get("argument_text")
        if not isinstance(template_name, str):
            raise ValueError(f"{field_name} record missing template_name")
        if not isinstance(argument_key, str):
            raise ValueError(f"{field_name} record missing argument_key")
        if not isinstance(argument_text, str):
            raise ValueError(f"{field_name} record missing argument_text")

        targets.append(
            {
                "template_name": template_name,
                "argument_key": argument_key,
                "argument_text": argument_text,
            }
        )

    return targets
