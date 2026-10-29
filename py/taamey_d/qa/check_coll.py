import collections

from collidoscope import Collidoscope

from taamey_d.qa.html_report import report_to_html, span_tf
from taamey_d.qa import check_helpers as hlp


def setup_collides(font_fna, cfg):
    cfgc = cfg.get("collidoscope")
    if not cfgc:
        return {}
    direction = cfg.get("direction") or "LTR"
    col = Collidoscope(font_fna, cfgc, direction=direction)
    # Below, we ask for the cfg (rules) back from col to make sure col
    # "understood" our config.
    # Otherwise, col might just be happily ignoring what we're asking
    # it to do.
    cfgc_ack = col.get_rules()  # ack: acknowledgment
    assert cfgc == cfgc_ack
    return {"collidoscope": col}


def renumber_clusters_sequentially(glyphs):
    # Collidoscope (as of 0.6.5) keeps HarfBuzz's cluster value, the index of
    # the cluster's first character, so neighbouring clusters differ by the
    # length of the earlier one. Its adjacent_clusters rule compares glyphs
    # whose clusters differ by less than 2, so with those values it compares
    # neighbouring letters only when the earlier one has no marks. Sequential
    # IDs make the rule compare every pair of neighbouring clusters.
    sequential_id, prev_cluster = 0, None
    for glyph in glyphs:
        if glyph["cluster"] != prev_cluster:
            sequential_id += 1
            prev_cluster = glyph["cluster"]
        glyph["cluster"] = sequential_id


def run_collides(ctx3, tcase):
    cfg, vhb, failed_tcases = ctx3["cfg"], ctx3["vhb"], ctx3["failed_tcases"]
    col = ctx3["extra_data"]["collidoscope"]
    shparams = hlp.get_shaping_parameters(tcase, cfg)
    tinput_str = hlp.tcase_input_str(tcase)
    output_buf = vhb.shape(tinput_str, shparams)
    glyphs = col.get_glyphs(tinput_str, buf=output_buf)
    renumber_clusters_sequentially(glyphs)
    collisions = col.has_collisions(glyphs)
    bumps = [f"{c.glyph1}/{c.glyph2}" for c in collisions]
    if bumps:
        draw = col.draw_overlaps(glyphs, collisions)
        failed_tcases.append((tinput_str, bumps, draw, output_buf))


def count_collision_types(failed_tcases):
    seen_bumps = collections.Counter()
    instance_nums = []
    for _, bumps, _, _ in failed_tcases:
        seen_bumps[tuple(bumps)] += 1
        instance_nums.append(seen_bumps[tuple(bumps)])
    return instance_nums, seen_bumps


def report_all_coll_fails(html_fp, ctx, failed_tcases):
    html_file, vhb = html_fp, ctx["vhb"]
    instance_nums, seen_bumps = count_collision_types(failed_tcases)
    fmtstr = "{} collision(s) ({} type(s)) found while shaping"
    msg1 = fmtstr.format(len(failed_tcases), len(seen_bumps))
    report_to_html(html_file, vhb, msg1, type="header")
    for failed_tcase, instance_num in zip(failed_tcases, instance_nums):
        shaping_text, bumps, draw, buf = failed_tcase
        max_instance_num = seen_bumps[tuple(bumps)]
        colstr = ",".join(bumps)
        blah_found_in = f"Instance {instance_num} of {max_instance_num} of {colstr} collision found in"
        msg2 = f"{blah_found_in} {span_tf(shaping_text)} <div>{draw}</div>"
        report_to_html(html_file, vhb, msg2, buf1=buf)


# The summary's measure of type is an unordered pair of colliding glyph names.
# It is coarser than count_collision_types' tuple of bumps, which also counts
# intersection points and both orders of each pair.
SUMMARY_INSTANCES_PER_TYPE = 3


def glyph_pairs(bumps):
    return sorted({"/".join(sorted(bump.split("/"))) for bump in bumps})


def report_coll_summary(html_fp, ctx, failed_tcases):
    html_file, vhb = html_fp, ctx["vhb"]
    by_pair = collections.defaultdict(list)
    for failed_tcase in failed_tcases:
        for pair in glyph_pairs(failed_tcase[1]):
            by_pair[pair].append(failed_tcase)
    fmtstr = "{} collision(s) ({} glyph pair(s)) found while shaping"
    msg1 = fmtstr.format(len(failed_tcases), len(by_pair))
    report_to_html(html_file, vhb, msg1, type="header")
    full_report = ctx["checkobj"].name + ".html"
    html_file.write(
        f"<p>Up to {SUMMARY_INSTANCES_PER_TYPE} instances of each unordered pair"
        " of colliding glyphs; a test case with several pairs is an instance of"
        f' each. Every instance: <a href="{full_report}">{full_report}</a></p>\n'
    )
    for pair, instances in sorted(by_pair.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        html_file.write(f"<h3>{pair}: {len(instances)} instance(s)</h3>\n")
        shown = instances[:SUMMARY_INSTANCES_PER_TYPE]
        for instance_num, (shaping_text, _, draw, buf) in enumerate(shown, 1):
            blah_found_in = f"Instance {instance_num} of {len(instances)} of {pair} collision found in"
            msg2 = f"{blah_found_in} {span_tf(shaping_text)} <div>{draw}</div>"
            report_to_html(html_file, vhb, msg2, buf1=buf)


def report_coll_fail(failed_tcase):
    shaping_text, bumps, _1, _2 = failed_tcase  # _1, _2 is draw, buf
    colstr = ",".join(bumps)
    return colstr, shaping_text


def checkobj_for_coll(font_fna):
    return hlp.CheckObj(
        "collides",
        "coll",
        run_collides,
        report_coll_fail,
        report_all_coll_fails,
        setup=setup_collides,
        report_summary_to_html=report_coll_summary,
    )
