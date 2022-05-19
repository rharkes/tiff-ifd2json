from ifd2json import ifd2json
pth_in = r'tests\test-input\multi-channel.ome.tif'
pth_out = r'tests\test-output-expected\multi-channel.IFDs.json'
ifd2json(pth_in, pth_out)
