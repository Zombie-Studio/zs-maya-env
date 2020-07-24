import pymel.core as pmc

class LPE(object):
    @property
    def beauty(self):
        return "C.*<L.>"

    @property
    def diffuse(self):
        return "C<TS>*<RD><L.>|<O.>"

    @property
    def diffuse_indirect(self):
        return "C<TS>*<RD>[DSV]+<L.>|<O.>"

    @property
    def scatter(self):
        return "C<TS>*<TD><L.>"

    @property
    def scatter_indirect(self):
        return "C<TS>*<TD>[DSVOB]+<L.>"

    @property
    def specular(self):
        return "C<TS>*<RS[^'coat']><L.>|<O.>"

    @property
    def specular_indirect(self):
        return "C<TS>*<RS[^'coat']>[DSV]+<L.>|<O.>"

    @property
    def coat(self):
        return "C<TS>*<RS'coat'><L.>|<O.>"

    @property
    def coat_indirect(self):
        return "C<TS>*<RS'coat'>[DSV]+<L.>|<O.>"

    def addLightGroup(self, lpe, lightgroup):
        # type: (str, str) -> str
        """
        Will return a LPE with a lightgroup tag add to light outputs
        :param lpe: Light path expression string
        :param lightgroup: Light group name to be added to original string
        :return: Resulting light path expression with added light group
        """
        return lpe.replace("<L.>", "<L.'{}'>".format(lightgroup))

