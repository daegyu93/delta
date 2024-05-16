import sys

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

def main(argv):

    file_save = True
    device_number = argv[1]
    video_path = "/dev/video" + str(device_number)

    try:
        save_file_name = argv[2]
    except:
        file_save = False
    Gst.init()
    config_file_path = "cam_"+str(device_number)+"/dewarper_config.txt"

    pipeline = Gst.Pipeline()
    width = 1920
    height = 1080
    framerate = 30
    
    nvv4l2camerasrc = Gst.ElementFactory.make("nvv4l2camerasrc", "nvv4l2camerasrc")
    nvv4l2camerasrc.set_property("device", video_path)

    caps_filter1  = Gst.ElementFactory.make("capsfilter", "capsfilter1")
    caps1 = Gst.Caps.from_string("video/x-raw(memory:NVMM),format=(string)UYVY, width=(int)%d, height=%d, framerate=%d/1"%(width, height, framerate))
    caps_filter1.set_property('caps', caps1)

    nvvidconv = Gst.ElementFactory.make("nvvideoconvert", "nvvideoconvert")

    caps_filter_dewarp  = Gst.ElementFactory.make("capsfilter", "caps_filter_dewarp")
    caps_dewarp = Gst.Caps.from_string("video/x-raw(memory:NVMM),format=(string)RGBA")
    caps_filter_dewarp.set_property('caps', caps_dewarp)

    nvdewarper = Gst.ElementFactory.make("nvdewarper", "nvdewarper")
    
    nvdewarper.set_property('config-file', config_file_path)


    nvvidconv2 = Gst.ElementFactory.make("nvvideoconvert", "nvvideoconvert2")

    caps_filter2 = Gst.ElementFactory.make("capsfilter", "capsfilter2")
    caps2 = Gst.Caps.from_string("video/x-raw(memory:NVMM),format=NV12,width=%d,height=%d,framerate=%d/1"%(width, height, framerate))
    caps_filter2.set_property('caps',caps2)

    tee = Gst.ElementFactory.make("tee", "t")

    queue1 = Gst.ElementFactory.make("queue", "queue1")
    nvegltransform = Gst.ElementFactory.make("nvegltransform", "nvegltransform")
    nveglglessink = Gst.ElementFactory.make("nveglglessink", "nveglglessink")
    nveglglessink.set_property("sync", False)
    nveglglessink.set_property("async", False)

    if file_save:
        queue2 = Gst.ElementFactory.make("queue", "queue2")
        nvv4l2h265enc = Gst.ElementFactory.make("nvv4l2h265enc", "nvv4l2h265enc")
        nvv4l2h265enc.set_property("bitrate", 10000000)

        h265parse = Gst.ElementFactory.make("h265parse", "h265parse")

        matroskamux = Gst.ElementFactory.make("matroskamux", "matroskamux")

        filesink = Gst.ElementFactory.make("filesink", "filesink")    
        filesink.set_property("location", save_file_name)

    tee.set_property("name", "t")


    pipeline.add(nvv4l2camerasrc)
    pipeline.add(caps_filter1)
    pipeline.add(nvvidconv)
    pipeline.add(caps_filter_dewarp)
    pipeline.add(nvdewarper)
    pipeline.add(nvvidconv2)
    pipeline.add(caps_filter2)
    pipeline.add(tee)
    pipeline.add(queue1)
    pipeline.add(nvegltransform)
    pipeline.add(nveglglessink)
    if file_save:
        pipeline.add(queue2)
        pipeline.add(nvv4l2h265enc)
        pipeline.add(h265parse)
        pipeline.add(matroskamux)
        pipeline.add(filesink)


    nvv4l2camerasrc.link(caps_filter1)
    caps_filter1.link(nvvidconv)
    nvvidconv.link(caps_filter_dewarp)
    caps_filter_dewarp.link(nvdewarper)
    nvdewarper.link(nvvidconv2)
    nvvidconv2.link(caps_filter2)
    caps_filter2.link(tee)


    tee.link(queue1)
    queue1.link(nvegltransform)
    nvegltransform.link(nveglglessink)
    if file_save:
        tee.link(queue2)
        queue2.link(nvv4l2h265enc)
        nvv4l2h265enc.link(h265parse)
        h265parse.link(matroskamux)
        matroskamux.link(filesink)

    pipeline.set_state(Gst.State.PLAYING)

    loop = GLib.MainLoop()

    # run
    try:
        loop.run()
    except KeyboardInterrupt:
        pipeline.set_state(Gst.State.NULL)
        loop.quit()

if __name__ == "__main__":
    main(sys.argv)